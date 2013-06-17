/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//require can.jquery-all

(function(can) {

can.Model.Cacheable("CMS.Models.Program", {
  root_object : "program"
  , root_collection : "programs"
  , findAll : "/api/programs?company_controls_first=true"
  , findOne : "/api/programs/{id}"
  , create : "POST /api/programs"
  , update : "PUT /api/programs/{id}"
  , init : function() {
    this.validatePresenceOf("title");
    this._super.apply(this, arguments);
  }
}, {});

can.Model.Cacheable("CMS.Models.Directive", {
  root_object : "directive"
  , root_collection : "directives"
  , findAll : "/api/directives"
  , findOne : "/api/directives/{id}"
  , create : "POST /api/directives"
}, {
  init : function() {
    this._super && this._super.apply(this, arguments);
    var that = this;
    this.attr("sections") || this.attr("sections", new CMS.Models.Section.List());
    this.attr("descendant_sections", can.compute(function() {
      return that.attr("sections").concat(can.reduce(that.sections, function(a, b) {
        return a.concat(can.makeArray(b.descendant_sections()));
      }, []));
    }));
    this.attr("descendant_sections_count", can.compute(function() {
      return that.attr("descendant_sections")().length;
    }));
  }
  , lowercase_kind : function() { return this.kind.toLowerCase(); }

});

CMS.Models.Directive("CMS.Models.Regulation", {
  findAll : "/api/directives?kind=Regulation"
  , create : {
    type : "POST"
    , url : "/api/directives"
    , data : {
      kind : "regulation"
    }
  }
}, {});

CMS.Models.Directive("CMS.Models.Policy", {
  findAll : "/api/directives?kind=Company+Policy"
  , create : {
    type : "POST"
    , url : "/api/directives"
    , data : {
      kind : "policy"
    }
  }
}, {});

CMS.Models.Directive("CMS.Models.Contract", {
  findAll : "/api/directives?kind=Contract"
  , create : {
    type : "POST"
    , url : "/api/directives"
    , data : {
      kind : "contract"
    }
  }
}, {});

can.Model.Cacheable("CMS.Models.OrgGroup", {
  root_object : "org_group"
  , root_collection : "org_groups"
  , findAll : "/api/org_groups"
  , create : "POST /api/org_groups"
}, {});

can.Model.Cacheable("CMS.Models.Project", {
  root_object : "project"
  , root_collection : "projects"
  , findAll : "/api/projects"
  , create : "POST /api/projects"
}, {});

can.Model.Cacheable("CMS.Models.Facility", {
  root_object : "facility"
  , root_collection : "facilities"
  , findAll : "/api/facilities"
  , create : "POST /api/facilities"
}, {});

can.Model.Cacheable("CMS.Models.Product", {
  root_object : "product"
  , root_collection : "products"
  , findAll : "/api/products"
  , create : "POST /api/products"
}, {});

can.Model.Cacheable("CMS.Models.DataAsset", {
  root_object : "data_asset"
  , root_collection : "data_assets"
  , findAll : "/api/data_assets"
  , create : "POST /api/data_assets"
}, {});

can.Model.Cacheable("CMS.Models.Market", {
  root_object : "market"
  , root_collection : "markets"
  , findAll : "/api/markets"
  , create : "POST /api/markets"
}, {});

can.Model.Cacheable("CMS.Models.RiskyAttribute", {
  root_object : "risky_attribute"
  , root_collection : "risky_attributes"
  , findAll : "/api/risky_attributes"
  , create : "POST /api/risky_attributes"
}, {});

can.Model.Cacheable("CMS.Models.Risk", {
  root_object : "risk"
  , root_collection : "risks"
  , findAll : function(params) {
    var root_object =  this.root_object
    , root_collection = this.root_collection;
    return $.ajax({
      url : "/api/risks"
      , type : "get"
      , data : params
      , dataType : "json"
    }).then(function(risks) {
      if(risks[root_collection + "_collection"]) {
        risks = risks[root_collection + "_collection"];
      }
      if(risks[root_collection]) {
        risks = risks[root_collection];
      }

      can.each(risks, function(r) {
        if(r[root_object]) {
          r = r[root_object];
        }
        if(r.hasOwnProperty("trigger")) {
          r.risk_trigger = r.trigger;
          delete r.trigger;
        }
      });
      return risks;
    });
  }
  , create : function(params) {
    params.trigger = params.risk_trigger;
    return $.ajax({
      type : "POST"
      , url : "/api/risks"
      , data : params
      , dataType : "json"
    });
  }
}, {});

can.Model.Cacheable("CMS.Models.Help", {
  root_object : "help"
  , root_collection : "helps"
  , findAll : "GET /api/help"
  , findOne : "GET /api/help/{id}"
  , update : "PUT /api/help/{id}"
  , create : "POST /api/help"
}, {});

can.Model.Cacheable("CMS.Models.Relationship", {
    root_object: "relationship"
  , root_collection: "relationships"
  , findAll: "GET /api/relationships"
  , create: function(params) {
      var _params = {
          relationship: {
              source: {
                  id: params.relationship.source_id
                , type: params.relationship.source_type
                }
            , destination: {
                  id: params.relationship.destination_id
                , type: params.relationship.destination_type
                }
            , relationship_type_id: params.relationship.relationship_type_id
          }
      };

      return $.ajax({
          type: "POST"
        , url: "/api/relationships"
        , dataType: "json"
        , data: _params
      });
    }
  , destroy: "DELETE /api/relationships/{id}"
}, {
    init: function() {
        var _super = this._super;
        function reinit() {
            var that = this;

            typeof _super === "function" && _super.call(this);
            this.attr("source", CMS.Models.get_instance(
                  this.source_type || this.source.type,
                  this.source_id || this.source.id));
            this.attr("destination", CMS.Models.get_instance(
                  this.destination_type || this.destination.type,
                  this.destination_id || this.destination.id));

            this.each(function(value, name) {
              if (value === null)
              that.removeAttr(name);
            });
        }

        this.bind("created", can.proxy(reinit, this));

        reinit.call(this);
    }
  , destroy: function() {
      return $.ajax({
        url: "/api/relationships/" + this.id
      , headers: {
          "If-Match": this.etag
        , "If-Unmodified-Since": this['last-modified']
        }
      , type: "DELETE"
      })
    }
});

CMS.Models.get_instance = function(object_type, object_id, params_or_object) {
  var model = CMS.Models[object_type]
    , params = {}
    ;

  if (!model)
    return null;

  params.id = object_id;

  if (!!params_or_object) {
    if ($.isFunction(params_or_object.serialize))
      $.extend(params, params_or_object.serialize());
    else
      $.extend(params, params_or_object || {});
  }

  return model.findInCacheById(object_id) || new model(params)
};

CMS.Models.get_link_type = function(instance, attr) {
  var type
    , model
    ;

  type = instance[attr + "_type"];
  if (!type) {
    model = instance[attr] && instance[attr].constructor;
    if (model)
      type = model.shortName;
    else
      type = instance[attr].type;
  }
  return type;
};

})(this.can);
