//require can.jquery-all

(function(can) {

can.Model.Cacheable("CMS.Models.Program", {
  root_object : "program"
  , root_collection : "programs"
  , findAll : "/api/programs?company_controls_first=true"
  , findOne : "/api/programs/{id}"
  , create : "POST /api/programs"
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
  findAll : "/api/directives?meta_kind=regulation"
  , create : {
    type : "POST"
    , url : "/api/directives"
    , data : {
      kind : "regulation"
    }
  }
}, {});

CMS.Models.Directive("CMS.Models.Policy", {
  findAll : "/api/directives?meta_kind=policy"
  , create : {
    type : "POST"
    , url : "/api/directives"
    , data : {
      kind : "policy"
    }
  }
}, {});

CMS.Models.Directive("CMS.Models.Contract", {
  findAll : "/api/directives?meta_kind=contract"
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
}, {});

can.Model.Cacheable("CMS.Models.Project", {
  root_object : "project"
  , root_collection : "projects"
  , findAll : "/api/projects"
}, {});

can.Model.Cacheable("CMS.Models.Facility", {
  root_object : "facility"
  , root_collection : "facilities"
  , findAll : "/api/facilities"
}, {});

can.Model.Cacheable("CMS.Models.Product", {
  root_object : "product"
  , root_collection : "products"
  , findAll : "/api/products"
}, {});

can.Model.Cacheable("CMS.Models.DataAsset", {
  root_object : "data_asset"
  , root_collection : "data_assets"
  , findAll : "/api/data_assets"
}, {});

can.Model.Cacheable("CMS.Models.Market", {
  root_object : "market"
  , root_collection : "markets"
  , findAll : "/api/markets"
}, {});

can.Model.Cacheable("CMS.Models.RiskyAttribute", {
  root_object : "risky_attribute"
  , root_collection : "risky_attributes"
  , findAll : "/api/risky_attributes"
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
}, {});

can.Model.Cacheable("CMS.Models.Help", {
  root_object : "help"
  , findAll : "GET /api/help"
  , findOne : "GET /api/help/{id}"
  , update : "PUT /api/help/{id}"
}, {});

})(this.can);