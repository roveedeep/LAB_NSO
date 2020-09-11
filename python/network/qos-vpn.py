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
        service.policy_name = 'VRF-'+str(service.shaper_size)+'MB-OUT'
        bps = service.shaper_size * 100000
        vars.add('bps', bps)

        self.log.info(service.DSCP_STANDARD_OUT.bandwidth )
        if service.DSCP_STANDARD_OUT.bandwidth > 0 :
            vars.add('s_bandwidth' , 'true')

        if service.DSCP_BUSINESS_OUT.bandwidth > 0 :
            vars.add('b_bandwidth' , 'true')

        if service.DSCP_VOICE_OUT.bandwidth > 0 :
            vars.add('vo_bandwidth' , 'true')

        if service.DSCP_VIDEO_OUT.bandwidth > 0 :
            vars.add('vi_bandwidth' , 'true')

        if service.DSCP_INTERACTIVE_OUT.bandwidth > 0 :
            vars.add('i_bandwidth' , 'true')

        if service.DSCP_STANDARD_OUT.bandwidth == 0 :
            vars.add('s_bandwidth' , 'false')

        if service.DSCP_BUSINESS_OUT.bandwidth == 0 :
            vars.add('b_bandwidth' , 'false')

        if service.DSCP_VOICE_OUT.bandwidth == 0 :
            vars.add('vo_bandwidth' , 'false')

        if service.DSCP_VIDEO_OUT.bandwidth == 0 :
            vars.add('vi_bandwidth' , 'false')

        if service.DSCP_INTERACTIVE_OUT.bandwidth == 0 :
            vars.add('i_bandwidth' , 'false')


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
