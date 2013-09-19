#####################################################################################
# PROJECT      : AuShadha
# Description  : AuShadhaBaseModel and AuShadhaBaseModelForm which all models inherit
# Author       : Dr. Easwar T R
# Date         : 16-09-2013
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
#####################################################################################

from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms

from django.utils import simplejson
from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder

import AuShadha.settings

from utilities.urls import generic_url_maker, UrlGenerator, urlgenerator_factory
from core.serializers.data_grid import generate_json_for_datagrid

from clinic.models import Clinic

#def generic_url_maker(instance, action, id, root_object=False):
    #"""
      #Returns the URL Pattern for any AuShadha Object
      #Following the naming conventions
      #instance   : an instance of a Django Model
      #action     : action that URL will commit : add/edit/delete/list/
      #root_object: for the list option is root_object is False, instance id will be appended to URL else no id
                   #will be appended.
                   #Eg:: to list all patients, under a clinic once a queryset is done
                   #the id will be that of the clinic. But for the root object clinic since there is no db_relationship
                   #that fetches a list of clinics, all clinics are fetched and listed.
    #"""
    ## FIXME:: may be better to rely on django.contrib.contenttypes.ContentType
    ## to do a similar thing rather than using _meta
    #from AuShadha.settings import APP_ROOT_URL
    #if not root_object:
        ##url = unicode(APP_ROOT_URL) + unicode(instance._meta.app_label)+ "/" + unicode(action) +"/" + unicode(id) +"/"
        #url = unicode(APP_ROOT_URL)              + \
            #unicode(instance._meta.app_label)  + "/" + \
            #unicode(instance.__model_label__)  + "/" + \
            #unicode(action) + "/" + unicode(id) + "/"
    #if root_object:
        #url = unicode(APP_ROOT_URL) + unicode(
            #instance._meta.app_label) + "/" + unicode(action) + "/"
    #return url


#def generate_json_for_datagrid(obj, success=True, error_message="Saved Successfully", form_errors=None):
    #"""Returns the JSON formatted Values of a specific Django Model Instance
    #for use with Dojo Grid. A few default DOJO Grid Values are specified, rest
    #are instance specific and are generated on the fly. It assumes the presence
    #of get_edit_url and get_del_url in the model instances passed to it via
    #obj.

    #ARGUMENTS: obj           : model instace / queryset
               #success       : A success message
               #error_message : Error Message if any.
               #form_errors   : Form Validation Errors from Django while saving can be passed.

    #"""
    #print "TRYING TO RETURN JSON FOR OBJECT: ", obj
    #json_data = []

    #try:
        #iterable = iter(obj)
        #if iterable:
            #for element in obj:
                #print element._meta.fields
                #data = {'success': success,
                        #'error_message': unicode(error_message),
                        #'form_errors': form_errors,
                        #'edit': getattr(element, 'get_edit_url()', element.get_edit_url()),
                        #'del': getattr(element, 'get_del_url()', element.get_del_url()),
                        #'patient_detail': getattr(element, 'patient_detail.__unicode__()', None)
                        #}
                #for i in element._meta.fields:
                    #print "CURRENT ITERATING FIELD NAME IS : ", i
                    #print "DATA DICTIONARY NOW IS ", data.keys()
                    #if i.name not in data.keys():
                        #print "Adding ", i.name
                        #print i.name.__class__
                        #data[i.name] = getattr(element, i.name, None)
                #json_data.append(data)

    #except TypeError:
        #print obj._meta.fields
        #data = {'success': success,
                #'error_message': unicode(error_message),
                #'form_errors': form_errors,
                #'edit': getattr(obj, 'get_edit_url()', obj.get_edit_url()),
                #'del': getattr(obj, 'get_del_url()', obj.get_del_url()),
                #'patient_detail': getattr(obj, 'patient_detail.__unicode__()', None)
                #}
        #for i in obj._meta.fields:
            #print "CURRENT ITERATING FIELD NAME IS : ", i
            #print "DATA DICTIONARY NOW IS ", data.keys()
            #if i.name not in data.keys():
                #print "Adding ", i.name
                #print i.name.__class__
                #data[i.name] = getattr(obj, i.name, None)
        #json_data.append(data)

    #json_data = simplejson.dumps(json_data, cls=DjangoJSONEncoder)
    #print "RETURNED JSON IS ", unicode(json)
    #return json_data


class AuShadhaBaseModel(models.Model):

    """
      Base AuShadha Model From which all AuShadha Models Except the Clinic
      Model Derive.
    """

    __model_label__ = "AuShadhaBaseModel"

    _parent_model = None    
    
    urls = {
            'summary':{},
            'tree'   :{},
            'sidebar':{},
            'json'   :{},
            'list'   :{},
            'add'    :{},
            'edit'   :{},
            'del'    :{},
    }

    def __init__(self, *args, **kwargs):

        super(AuShadhaBaseModel, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):

        super(AuShadhaBaseModel, self).save(*args, **kwargs)
        self.generate_urls()


    def __unicode__(self):

        return self.__model_label__

    def _generate_and_assign_urls(self,parent):
      """ Generates and Assigns URL to the Model Object"""

      self.url = urlgenerator_factory(self,parent)

    def generate_urls(self):

      parent = getattr(self,'_parent_model',None)
      print "Parent Instance for URL is ", parent

      if parent:
        if type(parent) is str:
          parent_field = getattr(self,parent)
          print "Parent Fields for URL is ", parent_field
          self._generate_and_assign_urls(parent_field)        
        elif type(parent) is list:
          for item in parent:
            p_field = getattr(self,item)
            self._generate_and_assign_urls(p_field)
      else:
        raise Exception("NoParentModelURLError")

#  def get_add_url(self):
#    if self.patient_detail:
#      return  generic_url_maker(self, "add", self.patient_detail.id)
#    else:
#      return  generic_url_maker(self, "add", self.parent_clinic.id)

    # def get_absolute_url(self):
        # return  "/AuShadha/%s/%s/%d/"(self._meta.app_label,
        # self.__model_label__, self.id)


    def get_absolute_url(self):
        return None

    def get_formatted_obj(self):
        return None

    def get_edit_url(self):
        return generic_url_maker(self, "edit", self.id)

    def get_del_url(self):
        return generic_url_maker(self, "del", self.id)

    def get_object_json_url(self):
        return "/AuShadha/%s_json/%s/" % (self.__model_label__, self.id)

    def _field_list(self):
        self.field_list = []
        print self._meta.fields
        for field in self._meta.fields:
            self.field_list.append(field)
        return self.field_list

    def _formatted_obj_data(self):
        if not self.field_list:
            _field_list()
        str_obj = "<ul>"
        for obj in self._field_list:
            _str += "<li>" + obj + "<li>"
            str_obj += _str
        str_obj += "</ul>"
        return str_obj

    def generic_url_maker(self, action, id, root_object=False):
        """
          Returns the URL Pattern for any AuShadha Object
          Following the naming conventions
          instance   : an instance of a Django Model
          action     : action that URL will commit : add/edit/delete/list/
          root_object: for the list option is root_object is False, instance id will be appended to URL else no id
                       will be appended.
                       Eg:: to list all patients, under a clinic once a queryset is done
                       the id will be that of the clinic. But for the root object clinic since there is no db_relationship
                       that fetches a list of clinics, all clinics are fetched and listed.
        """
        # FIXME:: may be better to rely on
        # django.contrib.contenttypes.ContentType to do a similar thing rather
        # than using _meta
        from AuShadha.settings import APP_ROOT_URL
        if root_object:
            url = unicode(APP_ROOT_URL) + unicode(self._meta.app_label) + \
                "/" + \
                unicode(self.__model_label__) + "/" + unicode(
                    action) + "/"
        else:
            print ("APP LABEL FOR URL IS", unicode(self._meta.app_label))
            url = unicode(APP_ROOT_URL) + unicode(self._meta.app_label) + "/" + unicode(
                self.__model_label__) + "/" + unicode(action) + "/" + unicode(id) + "/"
        return url

    def generate_json_for_datagrid(self):
        """Returns the JSON formatted Values of a specific Django Model
        Instance for use with Dojo Grid.

        A few default DOJO Grid Values are specified, rest are instance
        specific and are generated on the fly. It assumes the presence
        of get_edit_url and get_del_url in the model instances passed to
        it via obj.

        """
        print "TRYING TO RETURN JSON FOR OBJECT: ", self
        json_data = []
        print self._meta.fields
        data = {'add': getattr(self, 'get_add_url()', None),
                'edit': getattr(self, 'get_edit_url()', self.get_edit_url()),
                'del': getattr(self, 'get_del_url()', self.get_del_url()),
                'patient_detail': getattr(self, 'patient_detail.__unicode__()', self.patient_detail.__unicode__())
                }
        for i in self._meta.fields:
            print "CURRENT ITERATING FIELD NAME IS : ", i
            print "DATA DICTIONARY NOW IS ", data.keys(), data.values()
            if i.name not in data.keys():
                print "Adding ", i.name
                print i.name.__class__
                print simplejson.dumps(i.name)
                if i.name == "aushadhabasemodel_ptr":
                    data[i.name] = "AuShadhaBaseModel"
                else:
                    data[i.name] = getattr(self, i.name, None)
#      json_data.append(data)

        json_data = simplejson.dumps(data, cls=DjangoJSONEncoder)
        print "RETURNED JSON IS ", unicode(json_data)
        return json_data


class AuShadhaBaseModelForm(ModelForm):

    """
    Base class for all AuShadha ModelForms.
    """

    dijit_fields = {}

    __form_name__ = "AuShadhaBaseModelForm"

    class Meta:
        model = AuShadhaBaseModel


    def __init__(self, *args, **kwargs):
        super(AuShadhaBaseModelForm, self).__init__(*args, **kwargs)
        self.generate_dijit_form()

    def generate_dijit_form(self):
        if self.dijit_fields:
            for field_name, value_dict in self.dijit_fields.iteritems():
                for prop_key, prop_val in value_dict.iteritems():
                    self.fields[field_name].widget.attrs[prop_key] = prop_val
        else:
            print "No Text Fields ! "
            raise Exception("No Dijisable Dictionary Supplied")

