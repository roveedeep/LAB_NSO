# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service


# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')
        vars = ncs.template.Variables()
#        vars.add('AS', as_nun)
        template = ncs.template.Template(service)
        if service.rplOUT != 'n/a':
            vars.add('rplOUT', 'true')

        elif service.rplOUT == 'n/a':
            vars.add('rplOUT', 'false')

        isp2 = ['uk1','uk2','uk3','uk4']
        isp3 = ['o1','o2','o3','o4']
        device = service.device
        if (device in isp2) == True:
            vars.add('AS', '4456')
            template.apply('bgp-vpn-template', vars)

        elif (device in isp3) == True:
            vars.add('AS', '5599')
            template.apply('bgp-vpn-template', vars)

        else:
            vars.add('AS', '36994')
            template.apply('bgp-vpn-template', vars)
# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('bgp-servicepoint', ServiceCallbacks)
        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
