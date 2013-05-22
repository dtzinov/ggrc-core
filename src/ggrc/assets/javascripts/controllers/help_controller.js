(function(can, $) {

can.Control("GGRC.Controllers.Help", {
  defaults : {
    help_content_view : GGRC.mustache_path + "/help/help_modal_content.mustache"
    , help_header_view : GGRC.mustache_path + "/help/help_modal_header.mustache"
  }
}, {
  init : function() {
    this.options.$header = this.element.find(".modal-header");
    this.options.$content = this.element.find(".modal-body");
    this.on();
    this.draw_help()
  }
  , draw_help : function() {
    var that = this;
    
    var dfd = CMS.Models.Help.findOne({ id : 1 }).done(function(h) {
      that.options.instance = h;
    });
    can.view(this.options.help_header_view, dfd).done(function(frag) {
      that.options.$header.find("h2").html(frag);
    });

    can.view(this.options.help_content_view, dfd).done(function(frag) {
      that.options.$content.html(frag).removeAttr("style");
      that.element.find('.wysihtml5').each(function() {
        $(this).cms_wysihtml5();
      });
    });
  }
  , "{$content} input.btn[name='commit'] click" : function(el, ev) {
    this.options.instance.attr("title", this.element.find("#help_title").val())
    .attr("content", this.element.find("#help_content").val())
    .save();
  }
});

})(window.can, window.can.$);