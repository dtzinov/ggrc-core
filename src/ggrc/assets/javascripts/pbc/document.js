/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all
//= require models/cacheable

(function(ns, can) {

can.Model.Cacheable("CMS.Models.Document", {
    root_object : "document"
    , root_collection : "documents"
    , findAll : "GET /api/documents"
    , create : function(params) {
        var _params = {
            document : {
                title : params.document.title
                , description : params.document.description
                , link : params.document.link
            }
        };
        return $.ajax({
            type : "POST"
            , "url" : "/api/documents"
            , dataType : "json"
            , data : _params
        });
    }
    , search : function(request, response) {
        return $.ajax({
            type : "get"
            , url : "/api/documents"
            , dataType : "json"
            , data : {s : request.term}
            , success : function(data) {
                response($.map( data, function( item ) {
                  return can.extend({}, item.document, {
                    label: item.document.title 
                          ? item.document.title 
                          + (item.document.link_url 
                            ? " (" + item.document.link_url + ")" 
                            : "")
                          : item.document.link_url
                    , value: item.document.id
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
        //     if(obj = CMS.Models.ObjectDocument.findInCacheById(this.id) && attr !== "id") {
        //         obj.attr(attr, newVal);
        //     }
        // });

        var that = this;

        this.each(function(value, name) {
          if (value === null)
            that.attr(name, undefined);
        });
    }

});


can.Model.Cacheable("CMS.Models.ObjectDocument", {
    root_object : "object_document"
    , root_collection : "object_documents"
    , findAll: "GET /api/object_documents"
    , create : function(params) {
        var _params = {
            object_document : {
              documentable: {
                id: params.object_document.documentable_id || params.xable_id
              , type: params.object_document.documentable_type || params.xable_type
              }
            , document: {
                id: params.object_document.document_id
              }
            , role : params.role
            }
        };

        return $.ajax({
            type : "POST"
            , "url" : "/api/object_documents"
            , dataType : "json"
            , data : _params
        });
    }
    , destroy : "DELETE /api/object_documents/{id}"
    , attributes : {
      document : "CMS.Models.Document.model"
    }
}, {
    init : function() {
        var _super = this._super;
        function reinit() {
            var that = this;

            typeof _super === "function" && _super.call(this);
            // this.attr("document", CMS.Models.get_instance(
            //       "Document", this.document_id || this.document.id));
            this.documentable_id &&
              this.attr("documentable", CMS.Models.get_instance(
                    this.documentable_type || this.documentable.type,
                    this.documentable_id || this.documentable.id));
            /*this.attr(
                "document"
                , CMS.Models.Document.findInCacheById(this.document_id)
                || new CMS.Models.Document(this.document && this.document.serialize ? this.document.serialize() : this.document));
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
        url: "/api/object_documents/" + this.id
      , headers: {
          "If-Match": this.etag
        , "If-Unmodified-Since": this['last-modified']
        }
      , type: "DELETE"
      })
    }
});

})(this, can);
