from uuid import uuid4
from django.conf import settings
from django.contrib.messages import get_messages
from django.http import HttpRequest

from nkunyim_iam.util.session import HttpSession


class HttpContext(HttpSession):

    def __init__(self, req: HttpRequest) -> None:
        super().__init__(req=req)
        
        self.data = {}
        
        role = None
        business = None
        user = self.get_user()
        
        menus = []
        
        alerts = []
        navs = []
        
        toolbox_name = "toolbox"
        toolbox_menus = []
        
        manage_name =  "manage"
        manage_menus = []
        
        system_name = "system"
        system_menus = []
        
        env = settings.NKUNYIM_ENV
        
        path = req.path.lower()
        paths = ['/']
        node = "index"

        if len(path) > 1 and path.strip('/') != "":
            paths = path.strip('/').split('/')
            node = paths[-1]
        
        page = {
            "path": path,
            "paths": paths,
            "node": node,
            'name': "{}Page".format(node.title())
        }
        
        pages = dict(settings.NKUNYIM_PAGES)
        
        app_data = self.get_app_data()
        exclude_keys = ['client_id', 'client_secret', 'grant_type', 'response_type', 'scope']
        for key in app_data.keys():
            if key in exclude_keys:
                continue
            
            self.data[key] = app_data[key]

        # Messaes
        messages = get_messages(request=req)
        alert_map = {
            "debug": "primary",
            "info": "info",
            "success": "success",
            "warning": "warning",
            "error": "danger",
        }
        for message in messages:
            alerts.append({
                "type": alert_map[message.tags],
                "message": str(message)
            })

        # Account and Role
        account = self.get_account()
        if account and 'role' in account:
            menus = account['menus']
            role = account['role']
            business = account['business']
            
            
        
        if user and 'is_superuser' in user and user['is_superuser']:
            menus.append(
               {
                "id": str(uuid4()),
                "node": "system", 
                "module": {
                    "id": str(uuid4()),
                    "name": "Xvix",
                    "title": "AutoFix",
                    "caption": "Manage auto-fix data",
                    "icon": "mdi mdi-auto-fix",
                    "path": "xvix",
                    "route": "#xvix",
                },
                "items": [],
                "is_active": True
            })

        for menu in menus:
            # Node
            if menu['node'] == toolbox_name:
                toolbox_menus.append(menu)
                
            if menu['node'] == manage_name:
                manage_menus.append(menu)
                
            if menu['node'] == system_name:
                system_menus.append(menu)

            # Menu
            m_name = menu['module']['name']
            m_path = menu['module']['path']
            m_key = "{}Page".format(str(m_name).title())
            m_val = "./{m}/home.{e}".format(m=str(m_path).lower(), e=env)
            pages[m_key] = m_val

            # Item
            if menu['items'] and len(menu['items']) > 0:
                for item in menu['items']:
                    i_name = item['page']['name']
                    i_path = item['page']['path']
                    i_key = "{}{}Page".format(str(m_name).title(), str(i_name).title())
                    i_val = "./{m}/{p}.{e}".format(m=str(m_path).lower(), p=str(i_path).lower(), e=env)
                    pages[i_key] = i_val

        if len(toolbox_menus) > 0:
            navs.append(
                {
                    "name": toolbox_name.title(),
                    "menus": toolbox_menus
                }
            )

        if len(manage_menus) > 0:
            navs.append(
                {
                    "name": manage_name.title(),
                    "menus": manage_menus
                }
            )
            
        if len(system_menus) > 0:
            navs.append(
                {
                    "name": system_name.title(),
                    "menus": system_menus
                }
            )
            
        self.data['page'] = page
        self.data['pages'] = pages
        self.data['navs'] = navs
        self.data['alerts'] = alerts
        
        if user and 'username' in user:
            self.data['user'] = user
            
            if self.get_subdomain() == "app":
                self.data['role'] = role
                self.data['business'] = business
                
                
    def get_data(self) -> dict:
        """
        Returns the context data.
        """
        return self.data