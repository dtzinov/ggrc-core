/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all
//= require models/cacheable

(function(ns, can) {

can.Model.Cacheable("CMS.Models.Person", {
   root_object : "person"
   , root_collection : "people"
   , findAll : "GET /api/people"
   , create : function(params) {
        var _params = {
            person : {
                name : params.person.name
                , email : params.person.ldap || params.person.email
                , company : params.person.company
                , company_id : params.company_id
            }
        };
        return $.ajax({
            type : "POST"
            , "url" : "/api/people"
            , dataType : "json"
            , data : _params
        });
    }
    , search : function(request, response) {
        return $.ajax({
            type : "get"
            , url : "/api/people"
            , dataType : "json"
            , data : {s : request.term}
            , success : function(data) {
                response($.map( data, function( item ) {
                  return can.extend({}, item.person, {
                    label: item.person.email
                    , value: item.person.id
                  });
                }));
            }
        });
    }
}, {
    init : function () {
        this._super && this._super();
        // this.bind("change", function(ev, attr, how, newVal, oldVal) {
        //     var obj;
        //     if(obj = CMS.Models.ObjectPerson.findInCacheById(this.id) && attr !== "id") {
        //         obj.attr(attr, newVal);
        //     }
        // });

        var that = this;

        this.each(function(value, name) {
          if (value === null)
            that.removeAttr(name);
        });
    }
});


can.Model.Cacheable("CMS.Models.ObjectPerson", {
    root_object : "object_person"
    , root_collection : "object_people"
    , findAll: "GET /api/object_people"
    , create : function(params) {
        var _params = {
            object_person : {
              personable: {
                id: params.object_person.personable_id || params.xable_id,
                type: params.object_person.personable_type || params.xable_type
              }
            , person: {
                id: params.object_person.person_id
              }
            , role : params.role
            }
        };
        return $.ajax({
            type : "POST"
            , "url" : "/api/object_people"
            , dataType : "json"
            , data : _params
        });
    }
    , update : function(id, object) {
        var _params = {
            object_person : {
              personable: {
                id: params.object_person.personable_id || params.xable_id,
                type: params.object_person.personable_type || params.xable_type
              }
            , person: {
                id: params.object_person.person_id
              }
            , role : params.role
            }
        };
        return $.ajax({
            type : "PUT"
            , "url" : "/api/object_people/" + id
            , dataType : "json"
            , data : _params
        });
    }
    , destroy : "DELETE /api/object_people/{id}"
}, {
    init : function() {
        var _super = this._super;
        function reinit() {
            var that = this;

            typeof _super === "function" && _super.call(this);
            this.attr("person", CMS.Models.get_instance(
                  "Person", this.person_id || (this.person && this.person.id)));
            this.attr("personable", CMS.Models.get_instance(
                  this.personable_type || (this.personable && this.personable.type),
                  this.personable_id || (this.personable && this.personable.id)));
            /*this.attr(
                "person"
                , CMS.Models.Person.findInCacheById(this.person_id)
                || new CMS.Models.Person(this.person && this.person.serialize ? this.person.serialize() : this.person));
*/
            this.each(function(value, name) {
              if (value === null)
              that.removeAttr(name);
            });
        }

        this.bind("created", can.proxy(reinit, this));

        reinit.call(this);
    },
    destroy: function() {
      return $.ajax({
        url: "/api/object_people/" + this.id
      , headers: {
          "If-Match": this.etag
        , "If-Unmodified-Since": this['last-modified']
        }
      , type: "DELETE"
      })
    }
});

})(this, can);
