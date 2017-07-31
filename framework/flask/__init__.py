# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2017/4/1 8:59
"""

from app import app
from framework.utils import package_import

package_import("app.views")
package_import("framework.flask.errors")
package_import("framework.flask.intercept")
package_import("app.intercept")
