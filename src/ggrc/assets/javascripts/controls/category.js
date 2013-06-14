/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all
//= require models/cacheable

can.Model.Cacheable("CMS.Models.Category", {
  root_object : "category"
  , root_collection : "categories"
  ,  findAll : "GET /api/categories"
  , findTree : function(params) {
    var root_object = this.root_object
    , root_collection = this.root_collection
    , that = this;

    function filter_out(original, predicate) {
      var target = [];
      for(var i = original.length - 1; i >= 0; i--) {
        if(predicate(original[i])) {
          target.unshift(original.splice(i, 1)[0]);
        }
      }
      return target;
    }

    function treeify(list, pid) {
      var ret = filter_out(list, function(s) { return (!s.parent && !pid) || (s.parent && (s.parent.id == pid)); });
      // can.$(ret).each(function() {
      //   this.children = treeify(list, this.id);
      // });
      return ret;
    }

    return this.findAll(params).then(
      function(list, xhr) {
        list = list[root_collection + "_collection"]
        ? list[root_collection + "_collection"]
        : list;
       list = list[root_collection]
        ? list[root_collection]
        : list;

        can.$(list).each(function(i, s) {
          can.extend(s, s[root_object]);
          delete s[root_object];
        });
        var roots = treeify(list); //empties the list
        // for(var i = 0; i < roots.length; i++)
        //   list.push(roots[i]);
        roots.push(that.findInCacheById(-1));
        return roots;
    });
  }
  , attributes : {
    children : "CMS.Models.Category.models"
    , controls : "CMS.Models.Control.models"
  }
  , serialize : {
    "CMS.Models.Category.models" : function(val, type) {
      return can.map(val, function(v) {
        return {id : v.id, href : v.selfLink || v.href};
      });
    }
  }
  , tree_view_options : {
    list_view : "/static/mustache/controls/categories_tree.mustache"
    , start_expanded : false
    , child_options : [{
      model : null
      , property : "children"
    }, {
      model : CMS.Models.Control
      , property : "controls"
      , list_view : "/static/mustache/controls/tree_with_section_mappings.mustache"
    }]

  }
  , init : function() {
    this._super && this._super.apply(this, arguments);
    this.tree_view_options.child_options[0].model = this;

    this.validatePresenceOf("title");

    can.getObject("cache", this, true)[-1] = this.model({ id : -1, name : "Uncategorized Controls", controls : [] });
  }
}, {
  init : function() {
    var that = this;
    this._super && this._super.apply(this, arguments);

    this.attr("descendant_controls", can.compute(function() {
      return that.attr("controls").concat(can.reduce(that.attr("children"), function(a, b) {
        return a.concat(can.makeArray(b.descendant_controls()));
      }, []));
    }));
  }
});