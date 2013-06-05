/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

(function(can, $) {

GGRC.Controllers.Modals("GGRC.Controllers.Help", {
  defaults : {
    content_view : GGRC.mustache_path + "/help/help_modal_content.mustache"
    , header_view : GGRC.mustache_path + "/help/help_modal_header.mustache"
    , model : CMS.Models.Help
    , edit_btn_active : false
  }
}, {
  init : function() {
    //this.options.edit_btn_active = can.compute(this.options.edit_btn_active);
    this._super();
  }

  , "{$content} input.btn[name='commit'] click" : function(el, ev) {
    this.options.instance.save();
  }

  , "{$header} .help-edit click" : function(el, ev) {
    var that = this;
    setTimeout(function() {
      that.options.edit_btn_active = that.options.$content.find("#helpedit").is(".in");
    }, 10);
  }

  , find_params : function() {
    return {slug : this.options.slug};
  }
});

})(window.can, window.can.$);