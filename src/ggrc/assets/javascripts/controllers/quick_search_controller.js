/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//require can.jquery-all

(function(can, $) {
  function with_params(href, params) {
    if (href.charAt(href.length - 1) === '?')
      return href + params;
    else if (href.indexOf('?') > 0)
      return href + '&' + params;
    else
      return href + '?' + params;
  }

CMS.Controllers.Filterable("CMS.Controllers.QuickSearch", {
  defaults : {
    list_view : "/static/mustache/dashboard/object_list.mustache"
  }
}, {

  setup : function(el, opts) {
    this._super && this._super.apply(this, arguments);
    if(!opts.observer) {
      opts.observer = new can.Observe();
    }
  }

  , init : function(opts) {
    var that = this;
    var $tabs = this.element.find('ul.nav-tabs:first > li > a');
    $tabs.each(function(i, tab) {
      var $tab = $(tab)
      , href = $tab.attr('href') || $tab.data('tab-href')
      , loaded = $tab.data('tab-loaded')
      , pane = ($tab.data('tab-target') || $tab.attr('href'))
      , template = $tab.data("template") || "<div></div>"
      , model_name = $tab.attr("data-model") || $tab.attr("data-object-singular")
      , model = can.getObject("CMS.Models." + model_name) || can.getObject("GGRC.Models." + model_name)
      , view_data = new can.Observe({
        list: new model.List()
        //, list_view : template
        , observer: that.options.observer
        //, tooltip_view : not currently used -- href to tooltip instead
      });

      $tab.data("view_data", view_data);

      if(model) {
        $tab.data("model", model);
        model.findAll().done(function(data) {
          if($tab.is("li.active a")) {
            can.Observe.startBatch();
            view_data.attr('list', data);
            can.Observe.stopBatch();
          } else {
            setTimeout(function() {
              view_data.attr("list", data);
            }, 100);
          }
          $tab.find(".item-count").html(data ? data.length : 0);
        });

        model.bind("created", function(ev, instance) {
          view_data.list.unshift(instance.serialize());
        });
      }

      var spinner = new Spinner({ }).spin();
      $(pane).html(spinner.el);
      // Scroll up so spinner doesn't get pushed out of visibility
      $(pane).scrollTop(0);
      $(spinner.el).css({ width: '100px', height: '100px', left: '50px', top: '50px', zIndex : calculate_spinner_z_index });

      can.view(template /*GGRC.mustache_path + "/dashboard/quick_search_results.mustache"*/, view_data, function(frag, xhr) {
        $tab.data('tab-loaded', true);
        $(pane).html(frag).trigger("loaded", xhr, $tab.data("list"));
      });
    });
  }

  , "{observer} value" : function(el, ev, newval) {
    this.filter(newval);
    this.element.trigger('kill-all-popovers');
  }

  // @override
  , redo_last_filter : function(id_to_add) {
    var that = this;
    var $tabs = $(this.element).find('ul.nav-tabs:first > li > a');
    var old_sel = this.options.filterable_items_selector;
    var old_ids = this.last_filter_ids;

    $tabs.each(function(i, tab) {
      var $tab = $(tab)
      , model = $tab.data("model")
      , res = old_ids ? that.last_filter.getResultsFor(model) : null;

      that.options.filterable_items_selector = $($tab.attr("href") || $tab.attr("data-href")).find("li");
      that.last_filter_ids = res = res ? can.unique(can.map(res, function(v) { return v.id; })) : null; //null is the show-all case
      that._super();
      // res = can.map(res, function(obj, i) {
      //   var m = new model(obj);
      //   if(!m.selfLink) {
      //     m.refresh();
      //   }
      //   return m;
      // });
      $tab.find(".item-count").html(res ? res.length : $tab.data("view_data").list.length);
    });
  }

  , ".tabbable loaded" : function(el, ev) {
    $(el).scrollTop(0);
  }

  , ".nav-tabs li click" : function(el, ev) {
    var plural = el.children("a").attr("data-object-plural");
    var singular = can.map(window.cms_singularize(plural).split("_"), can.capitalize).join(" ");
    el.closest(".widget").find(".object-type").text(singular)
      .closest("a").attr("data-object-plural", plural.split(" ").join("_").toLowerCase())
      .attr("data-object-singular", singular);
  }

});

})(this.can, this.can.$);
