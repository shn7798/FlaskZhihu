# -*- coding: utf-8 -*-
from FlaskZhihu.application import create_app
from FlaskZhihu.settings import TestSettings, IPythonSettings
if __name__ == '__main__':
    settings = IPythonSettings()
    app = create_app(settings=settings)
    app.run(host='0.0.0.0')
