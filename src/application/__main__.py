#from application.app import model

#print('точка входа', end='\n\n')

#from . import app
#print(app, end='\n\n')
#print(app.model, end='\n\n')
#print(app.model.utils, end='\n\n')
#print(app.model.utils.ROOT_DIR, end='\n\n')

from application.app import controller
from application.app import view


if __name__ == '__main__':
    
    app = controller.Application()
    root = view.RootWidget(app)
    app.link_view(root)
    
    app.run()



