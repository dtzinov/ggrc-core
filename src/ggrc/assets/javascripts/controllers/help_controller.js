(function(can, $) {

GGRC.Controllers.Modals("GGRC.Controllers.Help", {
  defaults : {
    content_view : GGRC.mustache_path + "/help/help_modal_content.mustache"
    , header_view : GGRC.mustache_path + "/help/help_modal_header.mustache"
    , model : CMS.Models.Help
  }
}, {
  "{$content} input.btn[name='commit'] click" : function(el, ev) {
    this.options.instance.attr("title", this.element.find("#help_title").val())
    .attr("content", this.element.find("#help_content").val())
    .save();
  }

  , find_params : function() {
    return {id : 1};
  }
});

})(window.can, window.can.$);