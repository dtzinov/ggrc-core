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
  , attributes : {
    sections : "CMS.Models.SectionSlug.models"
    , program : "CMS.Models.Program.model"
  }
  , model : function(attrs) {
    if(!attrs[this.root_object]) {
      attrs = { directive : attrs };
    }
    var kind = GGRC.infer_object_type(attrs) || CMS.Models.Directive;
    var m = this.findInCacheById(attrs.directive.id);
    if(!m || m.constructor !== kind) {
      //We accidentally created a Directive or haven't created a subtype yet.
      if(m) {
        delete CMS.Models.Directive.cache[m.id];
      }
      m = this._super.apply(kind, arguments);
    }
    this.cache[m.id] = m;
    return m;
  }
}, {
  init : function() {
    this._super && this._super.apply(this, arguments);
    var that = this;
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
  , defaults : {
    kind : "regulation"
  }
  , attributes : {
    sections : "CMS.Models.SectionSlug.models"
    , program : "CMS.Models.Program.model"
  }
  , meta_kinds : [ "Regulation" ]
  , cache : can.getObject("cache", CMS.Models.Directive, true)
}, {});

CMS.Models.Directive("CMS.Models.Policy", {
  findAll : "/api/directives?kind__in=Company+Policy,Org+Group+Policy,Data+Asset+Policy,Product+Policy,Contract-Related+Policy,Company+Controls+Policy"
  , defaults : {
    kind : "policy"
  }
  , attributes : {
    sections : "CMS.Models.SectionSlug.models"
    , program : "CMS.Models.Program.model"
  }
  , meta_kinds : [  "Company Policy", "Org Group Policy", "Data Asset Policy", "Product Policy", "Contract-Related Policy", "Company Controls Policy" ]
  , cache : can.getObject("cache", CMS.Models.Directive, true)
}, {});

CMS.Models.Directive("CMS.Models.Contract", {
  findAll : "/api/directives?kind=Contract"
  , defaults : {
    kind : "contract"
  }
  , attributes : {
    sections : "CMS.Models.SectionSlug.models"
    , program : "CMS.Models.Program.model"
  }
  , meta_kinds : [ "Contract" ]
  , cache : can.getObject("cache", CMS.Models.Directive, true)
}, {});

can.Model.Cacheable("CMS.Models.OrgGroup", {
  root_object : "orggroup"
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

})(this.can);
