import typing
import logging
import requests
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CachedResponse(Base):
    __tablename__ = 'cached_responses'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    response_text = Column(String)

class RefreshManager:
    def refresh(self, session: requests.Session):
        raise NotImplementedError('lalalalalalalalw')

    def __bool__(self) -> bool:
        return False

class RequestsHandler:
    def __init__(self, session: requests.Session, refresh_manager: RefreshManager):
        self.session = session
        self.refresh_manager = refresh_manager

        # Suppress SQLAlchemy logging output
        logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

        self.engine = create_engine('sqlite:///cached_responses.db', echo=False)
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def refresh_session(self):
        if self.refresh_manager:
            self.refresh_manager.refresh(session=self.session)

    def get(self, url: str, params: dict[str, str], raw_response=False, cache_flag : bool = True):
        if raw_response:
            response = self.session.get(url=url, params=params)
            
            return response
        cached_response = self.get_cached_response(url)
        if cached_response:
            return cached_response.response_text

        response = self.session.get(url=url, params=params)

        if response.status_code != 200:
            raise Exception("Something went whack!")

        if cache_flag:
            self.cache_response(url, response.text)
        return response.text
    def post(self, url: str, data: dict[str, str], raw_response=False):
        response = self.session.post(url=url, data=data)

        if response.status_code != 200:
            raise Exception("Something went whack!")

        if raw_response:
            return response.text
        return response.text
    def cache_response(self, url: str, response_text: str):
        session = self.Session()
        cached_response = CachedResponse(url=url, response_text=response_text)
        session.add(cached_response)
        session.commit()
        session.close()

    def get_cached_response(self, url: str):
        session = self.Session()
        cached_response = session.query(CachedResponse).filter_by(url=url).first()
        session.close()
        return cached_response

    @staticmethod
    def create_instance(authentication_dict: dict[str, str] | None,
                        authentication_get_callable: typing.Callable[[], str] | None = None) -> 'RequestsHandler':
        if authentication_get_callable:
            authentication_dict = authentication_get_callable()

        return create_requests_handler(authentication_dict=authentication_dict, refresh_manager=RefreshManager())

def create_requests_handler(authentication_dict: dict[str, str] | None, refresh_manager: RefreshManager) -> RequestsHandler:
    if authentication_dict is not None:
        proxy_username = authentication_dict['proxy_username']
        proxy_password = authentication_dict['proxy_password']
        proxy_url = authentication_dict['proxy_url']
        proxy_port = authentication_dict['proxy_port']

        session = requests.Session()
        auth = requests.HTTPProxyAuth(proxy_username, proxy_password)

        # Configure proxies for the session
        proxies = {
            'http': f'http://{proxy_username}:{proxy_password}@{proxy_url}:{proxy_port}',
            'https': f'http://{proxy_username}:{proxy_password}@{proxy_url}:{proxy_port}'
        }

        session.proxies.update(proxies)
        return RequestsHandler(session=session, refresh_manager=refresh_manager)

    with requests.Session() as session:
        return RequestsHandler(session=session, refresh_manager=refresh_manager)
