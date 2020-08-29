# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service
import ipaddress

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
        p_int, vlan = str(service.interface_name).split('.')
        switch_device = service.device
        vars.add('vlan', vlan)
        vars.add('shutdown', service.shutdown)
        vars.add('interface_name', service.interface_name)
        service.vlan = vlan
        service.pe_interface = str(service.interface_type) + service.interface_name
        template.apply('pe-int-template', vars)

        if ((service.device == 'm1' or service.device == 'm2') and (p_int=='1/0')):
            switch_device = ['sw1']
            for sw in switch_device:
                vars.add('switch_device', sw)
                template.apply('sw_vlan', vars)

        if ((service.device == 'm1' or service.device == 'm2') and (p_int =='0/3')):
            switch_device = ['sw3']
            for sw in switch_device:
                vars.add('switch_device', sw)
                template.apply('sw_vlan', vars)
#testing
        if service.device == 'h3' or service.device == 'h2':

            if p_int == '0/3' :
                sw = 'sw2'
                vars.add('switch_device', sw)
                template.apply('sw_vlan', vars)

            elif p_int == '1/0' :
                sw = 'sw4'
                vars.add('switch_device', sw)
                template.apply('sw_vlan', vars)


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
        self.register_service('vpn-servicepoint', ServiceCallbacks)
        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
