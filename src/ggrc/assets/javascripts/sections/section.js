/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all
//= require controls/control
//= require models/cacheable

can.Model.Cacheable("CMS.Models.Section", {
  root_object : "section"
  , root_collection : "sections"
  , findAll : "GET /api/sections?" + window.cms_singularize((/^\/([^\/]+)\//.exec(window.location.pathname) || ["",""])[1]) + ".id=" + (/^\/[^\/]+\/([^\/]+)/.exec(window.location.pathname) || ["",""])[1]
  , create : "POST /api/sections"
  , update : "PUT /api/sections/{id}"
  , attributes : {
    children : "CMS.Models.Section.model"
  }
  , defaults : {
    children : []
  }
  , map_control : function(params, section) {
    var control_section_ids, joins;

    if(params.u) {
      control_section_ids = can.map(params.control.control_sections, function(v) {
        return v.id;
      });

      joins = can.map(section.control_sections, function(sc) {
        return ~can.inArray(sc.id, control_section_ids) ? sc : undefined;
      });

      return $.when.apply($, can.map(joins, function(join) {
        return join.refresh().then(function(j) {
          return j.destroy();
        });
      }));
    } else {
      return new CMS.Models.ControlSection({
        section : section.stub()
        , control : params.control.stub()
      }).save();
    }

  }

}, {

  init : function() {

    this._super();

    var that = this;
    this.each(function(value, name) {
      if (value === null)
        that.removeAttr(name);
    });

    this.attr("descendant_sections", can.compute(function() {
      return that.attr("children").concat(can.reduce(that.children, function(a, b) {
        return a.concat(can.makeArray(b.descendant_sections()));
      }, []));
    }));
    this.attr("descendant_sections_count", can.compute(function() {
      return that.attr("descendant_sections")().length;
    }));
  }

  , map_control : function(params) {
    return this.constructor.map_control(
      can.extend({}, params, { section : this })
      , this);
  }

});

CMS.Models.Section("CMS.Models.SectionSlug", {
  attributes : {
    children : "CMS.Models.SectionSlug.models"
    , controls : "CMS.Models.Control.models"
    , control_sections : "CMS.Models.ControlSection.models"
  }
  ,  findAll : function(params) {
    function filter_out(original, predicate) {
      var target = [];
      for(var i = original.length - 1; i >= 0; i--) {
        if(predicate(original[i])) {
          target.unshift(original.splice(i, 1)[0]);
        }
      }
      return target;
    }

    function treeify(list, directive_id, pid) {
      var ret = filter_out(list, function(s) { 
        return (!s.parent && !pid) || (s.parent.id == pid && (!directive_id || (s.directive && s.directive.id === directive_id)));
      });
      can.$(ret).each(function() {
        this.children = treeify(list, this.directive ? this.directive.id : null, this.id);
      });
      return ret;
    }

    return this._super(params).pipe(
        function(list, xhr) {
          var current;
          can.$(list).each(function(i, s) {
            can.extend(s, s.section);
            delete s.section;
          });
          var roots = treeify(list); //empties the list if all roots (no parent in list) are actually roots (null parent id)
          // for(var i = 0; i < roots.length; i++)
          //   list.push(roots[i]);
          while(list.length > 0) {
            can.$(list).each(function(i, v) {
              // find a pseudo-root whose parent wasn't in the returned sections
              if(can.$(list).filter(function(j, c) { return c !== v && v.parent && c.id === v.parent.id && ((!c.directive && !v.directive) || (c.directive && v.directive && c.directive.id === v.directive.id)) }).length < 1) {
                current = v;
                list.splice(i, 1); //remove current from list
                return false;
              }
            });
            current.attr ? current.attr("children", treeify(list, current.id)) : (children = treeify(list, current.id));
            roots.push(current);
          }
          return roots;
        });
  }
  , tree_view_options : {
    list_view : "/static/mustache/sections/tree.mustache"
    , child_options : [{
      model : CMS.Models.Control
      , property : "controls"
      , list_view : "/static/mustache/controls/tree.mustache"
    }, {
      model : CMS.Models.SectionSlug
      , property : "children"
    }]
  }
  , init : function() {
    this._super.apply(this, arguments);
    this.tree_view_options.child_options[1].model = this;
    this.bind("created updated", function(ev, inst) {
      can.each(this.attributes, function(v, key) {
        (inst.key instanceof can.Observe.List) && inst.key.replace(inst.key); //force redraw in places
      });
    });
  }
}, {});

can.Model.Cacheable("CMS.Models.ControlSection", {
  root_collection : "control_sections"
  , root_object : "control_section"
  , create : "POST /api/control_sections"
  , destroy : "DELETE /api/control_sections/{id}"
  , init : function() {
    var that = this;
    this._super.apply(this, arguments);
    this.bind("created destroyed", function(ev, inst) {
      if(that !== inst.constructor) return;
      var section =
        CMS.Models.SectionSlug.findInCacheById(inst.section.id)
        || CMS.Models.Section.findInCacheById(inst.section.id);
      var control = 
        CMS.Models.RegControl.findInCacheById(inst.control.id)
        || CMS.Models.Control.findInCacheById(inst.control.id);

      section && section.refresh();
      control && control.refresh();
    });
  }
}, {
  serialize : function(name) {
    var serial;
    if(!name) {
      serial = this._super();
      serial.section && (serial.section = this.section.stub());
      serial.control && (serial.control = this.control.stub());
      return serial;
    } else {
      return this._super.apply(this, arguments);
    }
  }
});
