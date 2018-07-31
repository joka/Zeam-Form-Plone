
import Acquisition

from five import grok
from zeam.form.base.widgets import FieldWidget
from zeam.form.ztk.widgets.choice import ChoiceField
from zeam.form.ztk.widgets.collection import (
    CollectionField, newCollectionWidgetFactory, MultiGenericFieldWidget,
    MultiChoiceFieldWidget)
from zeam.form.ztk.widgets.text import TextField
from zeam.form.base.interfaces import IWidget
from zeam.form.ztk.interfaces import ICollectionField
from zope.interface import Interface
from Products.CMFPlone.resources import add_bundle_on_request, add_resource_on_request


class PloneFieldWidget(FieldWidget, Acquisition.Explicit):
    grok.baseclass()

    @property
    def context(self):
        # Plone Zope 2 template need a context.
        return self.form.context


class PloneWYSIWYGFieldWidget(PloneFieldWidget):
    grok.adapts(TextField, Interface, Interface)
    grok.name('plone.wysiwyg')


grok.global_adapter(
    newCollectionWidgetFactory(mode='plone.multi-select'),
    adapts=(ICollectionField, Interface, Interface),
    provides=IWidget,
    name='plone.multi-select')


class PloneMultiSelectFieldWidget(MultiChoiceFieldWidget, PloneFieldWidget):
    grok.adapts(CollectionField, ChoiceField, Interface, Interface)
    grok.name('plone.multi-select')

    def update(self):
        super(PloneMultiSelectFieldWidget, self).update()


generic_update = MultiGenericFieldWidget.update

def update_include(inst):
    generic_update(inst)
    add_resource_on_request(inst.request, 'json-template')
    add_resource_on_request(inst.request, 'reordering')
    add_resource_on_request(inst.request, 'zeam_widgets')
    
    
MultiGenericFieldWidget.update = update_include
    
