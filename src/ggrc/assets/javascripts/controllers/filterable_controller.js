/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all

(function(can, $) {

can.Control("CMS.Controllers.Filterable", {
  defaults : {
    filterable_items_selector : "[data-model]"
    , spinner_while_filtering : false
    , spinner_style : {
      top : 100
      , left : 100
      , height : 50
      , width : 50
      , position : "absolute"
    }
  }
  //static
}, {
  filter : function(str, extra_params, dfd) {
    var that = this
    , spinner
    , search_dfds = str ? [GGRC.Models.Search.search(str, extra_params)] : [$.when(null)];
    dfd && search_dfds.push(dfd);

    if(this.options.spinner_while_filtering) {
      spinner = new Spinner().spin();
      $(spinner.el).css(this.options.spinner_style);
      this.element.append(spinner.el);
    }
    return $.when.apply($, search_dfds).then(function(data) {
      var _filter = null, ids = null;
      if(data) {
        v_filter = that.options.model ? data.getResultsFor(that.options.model) : data.entries;
        ids = data ? can.map(data.entries, function(v) { return v.id; }) : null;
      }
      that.last_filter_ids = ids;
      that.last_filter = _filter;
      that.redo_last_filter();
      spinner && spinner.stop();
      return ids;
    });
  }

  , redo_last_filter : function(id_to_add) {
    id_to_add && this.last_filter_ids.push(id_to_add);
    var that = this;
    that.element.find(that.options.filterable_items_selector).each(function() {
      var $this = $(this);
      if(that.last_filter_ids == null || can.inArray($this.data("model").id, that.last_filter_ids) > -1)
        $this.show();
      else
        $this.hide();
    });
    return $.when(this.last_filter_ids);
  }

});

})(this.can, this.can.$);