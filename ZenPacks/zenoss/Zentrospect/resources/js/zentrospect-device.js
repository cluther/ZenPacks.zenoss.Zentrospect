(function(){

var ZC = Ext.ns('Zenoss.component');


/* Support for better ComponentGridPanels ***********************************/

Ext.apply(Zenoss.render, {
    zentrospect_entityLinkFromGrid: function(obj, col, record) {
        if (!obj)
            return;

        if (typeof(obj) == 'string')
            obj = record.data;

        if (!obj.title && obj.name)
            obj.title = obj.name;

        var isLink = false;

        if (this.refName == 'componentgrid') {
            // Zenoss >= 4.2 / ExtJS4
            if (this.subComponentGridPanel || this.componentType != obj.meta_type)
                isLink = true;
        } else {
            // Zenoss < 4.2 / ExtJS3
            if (!this.panel || this.panel.subComponentGridPanel)
                isLink = true;
        }

        if (isLink) {
            return '<a href="javascript:Ext.getCmp(\'component_card\').componentgrid.jumpToEntity(\''+obj.uid+'\', \''+obj.meta_type+'\');">'+obj.title+'</a>';
        } else {
            return obj.title;
        }
    }
});

ZC.ZentrospectComponentGridPanel = Ext.extend(ZC.ComponentGridPanel, {
    subComponentGridPanel: false,

    jumpToEntity: function(uid, meta_type) {
        var tree = Ext.getCmp('deviceDetailNav').treepanel;
        var tree_selection_model = tree.getSelectionModel();
        var components_node = tree.getRootNode().findChildBy(
            function(n) {
                if (n.data) {
                    return n.data.text == 'Components';
                }
                
                return n.text == 'Components';
            });
        
        var component_card = Ext.getCmp('component_card');
        
        if (components_node.data) {
            component_card.setContext(components_node.data.id, meta_type);
        } else {
            component_card.setContext(components_node.id, meta_type);
        }

        component_card.selectByToken(uid);
        var component_type_node = components_node.findChildBy(
            function(n) {
                if (n.data) {
                    return n.data.id == meta_type;
                }
                
                return n.id == meta_type;
            });
        
        if (component_type_node.select) {
            tree_selection_model.suspendEvents();
            component_type_node.select();
            tree_selection_model.resumeEvents();
        } else {
            tree_selection_model.select([component_type_node], false, true);
        }
    }
});


/* ComponentGridPanels ******************************************************/

ZC.ZentrospectSystemPanel = Ext.extend(ZC.ZentrospectComponentGridPanel, {
    subComponentGridPanel: false,

    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'name',
            componentType: 'ZentrospectSystem',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'status'},
                {name: 'severity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'locking'},
                {name: 'process_count'},
                {name: 'metric_count'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                renderer: Zenoss.render.zentrospect_entityLinkFromGrid
            },{
                id: 'process_count',
                dataIndex: 'process_count',
                header: _t('Processes'),
                width: 80
            },{
                id: 'metric_count',
                dataIndex: 'metric_count',
                header: _t('Metrics'),
                width: 80
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                width: 70
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 65
            }]
        });
        ZC.ZentrospectSystemPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('ZentrospectSystemPanel', ZC.ZentrospectSystemPanel);


ZC.ZentrospectProcessPanel = Ext.extend(ZC.ZentrospectComponentGridPanel, {
    subComponentGridPanel: false,

    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'name',
            componentType: 'ZentrospectProcess',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'status'},
                {name: 'severity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'locking'},
                {name: 'system'},
                {name: 'process_name'},
                {name: 'metric_count'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                renderer: Zenoss.render.zentrospect_entityLinkFromGrid
            },{
                id: 'system',
                dataIndex: 'system',
                header: _t('System'),
                renderer: Zenoss.render.zentrospect_entityLinkFromGrid,
                sortable: false,
                width: 120
            },{
                id: 'process_name',
                dataIndex: 'process_name',
                header: _t('Process'),
                width: 120
            },{
                id: 'metric_count',
                dataIndex: 'metric_count',
                header: _t('Metrics'),
                width: 80
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                width: 70
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 65
            }]
        });
        ZC.ZentrospectProcessPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('ZentrospectProcessPanel', ZC.ZentrospectProcessPanel);


ZC.ZentrospectMetricPanel = Ext.extend(ZC.ZentrospectComponentGridPanel, {
    subComponentGridPanel: false,

    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'name',
            componentType: 'ZentrospectMetric',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'status'},
                {name: 'severity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'locking'},
                {name: 'system'},
                {name: 'process'},
                {name: 'metric_name'},
                {name: 'value'},
                {name: 'cycles_old'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                renderer: Zenoss.render.zentrospect_entityLinkFromGrid
            },{
                id: 'system',
                dataIndex: 'system',
                header: _t('System'),
                renderer: Zenoss.render.zentrospect_entityLinkFromGrid,
                sortable: false,
                width: 120
            },{
                id: 'process',
                dataIndex: 'process',
                header: _t('Process'),
                renderer: Zenoss.render.zentrospect_entityLinkFromGrid,
                sortable: false,
                width: 120
            },{
                id: 'metric_name',
                dataIndex: 'metric_name',
                header: _t('Metric'),
                width: 120
            },{
                id: 'value',
                dataIndex: 'value',
                header: _t('Value'),
                width: 80
            },{
                id: 'cycles_old',
                dataIndex: 'cycles_old',
                header: _t('Cycles Old'),
                width: 90
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                width: 70
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 65
            }]
        });
        ZC.ZentrospectMetricPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('ZentrospectMetricPanel', ZC.ZentrospectMetricPanel);


/* Subcomponent Panels ******************************************************/

Zenoss.nav.appendTo('Component', [{
    id: 'component_processes',
    text: _t('Processes'),
    xtype: 'ZentrospectProcessPanel',
    subComponentGridPanel: true,
    filterNav: function(navpanel) {
        if (navpanel.refOwner.componentType == 'ZentrospectSystem') {
            return true;
        }

        return false;
    },
    setContext: function(uid) {
        ZC.ZentrospectProcessPanel.superclass.setContext.apply(this, [uid]);
    }
}]);


Zenoss.nav.appendTo('Component', [{
    id: 'component_metrics',
    text: _t('Metrics'),
    xtype: 'ZentrospectMetricPanel',
    subComponentGridPanel: true,
    filterNav: function(navpanel) {
        switch (navpanel.refOwner.componentType) {
            case 'ZentrospectSystem': return true;
            case 'ZentrospectProcess': return true;
            default: return false;
        }
    },
    setContext: function(uid) {
        ZC.ZentrospectMetricPanel.superclass.setContext.apply(this, [uid]);
    }
}]);


}());
