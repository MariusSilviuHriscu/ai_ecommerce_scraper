import typing
import requests

class RefreshManager:
    
    pass
    def refresh(self,session : requests.Session):
        raise NotImplementedError('lalalalalalalalw')
    
    def __bool__(self) -> bool:
        
        return False
    
class RequestsHandler:
    
    def __init__(self , session : requests.Session , refresh_manager : RefreshManager ):
        
        self.session = session
        self.refresh_manager = refresh_manager
    
    def refresh_session(self):
        if self.refresh_manager:
            self.refresh_manager.refresh(session = self.session)

    def get(self,url: str , params : dict[str,str], raw_response = False ):
        response = self.session.get(url = url ,params= params)
        
        if response.status_code != 200:
            raise Exception("Something went whack!")
        
        if raw_response:
            return response
        return response.text
    def post(self,url: str , params : dict[str,str], raw_response = False ):
    
        
        response = self.session.post( url , params)
        
        if response.status_code != 200:
            raise Exception("Something went whack!")
        
        if raw_response:
            return response
        return response.text
    @staticmethod
    def create_instance(authentification_dict:dict[str,str] | None,
                        authentification_get_callable : typing.Callable[[],str] | None = None
                            ) -> typing.Self :
        if authentification_get_callable:
            
            authentification_dict = authentification_get_callable()
        
        return create_requests_handler(authentification_dict = authentification_dict,
                                       refresh_manager = RefreshManager()
                                       )


def create_requests_handler(authentification_dict:dict[str,str] | None ,refresh_manager : RefreshManager) -> RequestsHandler:
    
    if authentification_dict is not None:
        proxy_username = authentification_dict['proxy_username']
        proxy_password = authentification_dict['proxy_password']
        proxy_url = authentification_dict['proxy_url']
        proxy_port = authentification_dict['proxy_port']
        
        session = requests.Session()
        auth = requests.HTTPProxyAuth(proxy_username, proxy_password)
        
        # Configure proxies for the session
        proxies = {
            'http': f'http://{proxy_username}:{proxy_password}@{proxy_url}:{proxy_port}',
            'https': f'http://{proxy_username}:{proxy_password}@{proxy_url}:{proxy_port}'
        }
        
        session.proxies.update(proxies)
        return RequestsHandler(session = session,
                               refresh_manager = refresh_manager
                               )

    
    with requests.Session() as session:
        return RequestsHandler(session = session,
                               refresh_manager = refresh_manager
                               )