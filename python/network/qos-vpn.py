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
        template = ncs.template.Template(service)
        service.policy_name = 'VRF-'+str.upper(service.shaper_size)+'-OUT'

        bps = service.shaper_size
        if ('k' in bps) == True:
            shaper,a = str(bps).split('k')
            bps = int(shaper)*10240
            self.log.info(bps)
            vars.add('bps', bps)

        if ('m' in str(bps)) == True:
            shaper,a = str(bps).split('m')
            bps = int(shaper)*1000000
            vars.add('bps', bps)

        if ('g' in str(bps)) == True:
            shaper,a = str(bps).split('m')
            bps = int(shaper)*1000000
            vars.add('bps', bps)


        if service.STANDARD != 'n/a' :
            vars.add('s_bandwidth' , 'true')
            vars.add('s' , service.STANDARD)

        if service.BUSINESS != 'n/a' :
            vars.add('b_bandwidth' , 'true')
            vars.add('s' , service.BUSINESS)

        if service.VOICE != 'n/a' :
            vars.add('vo_bandwidth' , 'true')
            vars.add('s' , service.VOICE)

        if service.VIDEO != 'n/a' :
            vars.add('vi_bandwidth' , 'true')

        if service.INTERACTIVE != 'n/a' :
            vars.add('i_bandwidth' , 'true')
            vars.add('s' , sservice.INTERACTIVE)

        if service.STANDARD == 0 or service.STANDARD =='n/a':
            vars.add('s_bandwidth' , 'false')
            vars.add('s' , '0')

        if service.BUSINESS == 0 or service.BUSINESS == 'n/a' :
            vars.add('b_bandwidth' , 'false')
            vars.add('b' , '0')

        if service.VOICE == 0 or service.VOICE == 'n/a' :
            vars.add('vo_bandwidth' , 'false')
            vars.add('vo' , '0')

        if service.VIDEO == 0 or service.VIDEO == 'n/a' :
            vars.add('vi_bandwidth' , 'false')
            vars.add('vi' , '0')

        if service.INTERACTIVE == 0 or service.INTERACTIVE == 'n/a'  :
            vars.add('i_bandwidth' , 'false')
            vars.add('i' , '0')


        template.apply('qos-template', vars)
        template.apply('qos-child-template', vars)

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
        self.register_service('qos-vpn-servicepoint', ServiceCallbacks)
        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
