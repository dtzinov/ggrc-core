(function(can, $) {

can.Control("GGRC.Controllers.Modals", {
  BUTTON_VIEW_DONE : GGRC.mustache_path + "/modals/done_buttons.mustache"
  , BUTTON_VIEW_CLOSE : GGRC.mustache_path + "/modals/close_buttons.mustache"
//  BUTTON_VIEW_SAVE
  , BUTTON_VIEW_SAVE_CANCEL : GGRC.mustache_path + "/modals/save_cancel_buttons.mustache"
//  BUTTON_VIEW_SAVE_CANCEL_DELETE

  , defaults : {
    content_view : GGRC.mustache_path + "/help/help_modal_content.mustache"
    , header_view : GGRC.mustache_path + "/modals/modal_header.mustache"
    , button_view : null
    , model : null
    , new_object_form : false
  }

  , init : function() {
    this.defaults.button_view = this.BUTTON_VIEW_DONE;
  }
}, {
  init : function() {
    this.options.$header = this.element.find(".modal-header");
    this.options.$content = this.element.find(".modal-body");
    this.options.$footer = this.element.find(".modal-footer");
    this.on();
    this.fetch_all();
  }

  , fetch_templates : function(dfd) {
    dfd = dfd || new $.Deferred();
    return $.when(
      can.view(this.options.content_view, dfd)
      , can.view(this.options.header_view, dfd)
      , can.view(this.options.button_view, dfd)
    ).done(this.proxy('draw'));
  }

  , fetch_data : function() {
    var that = this;
    var dfd = this.options.model && !this.options.new_object_form ?
                this.options.model.findOne(this.find_params())
              : new $.Deferred().resolve(this.find_params());

    return dfd.done(function(h) {
      that.options.instance = h;
    });
  }

  , fetch_all : function() {
    return this.fetch_templates(this.fetch_data(this.find_params()));
  }

  , find_params : function() {
    return this.options;
  }

  , draw : function(content, header, footer) {
    header != null && this.options.$header.find("h2").html(header);
    content != null && this.options.$content.html(content).removeAttr("style");
    footer != null && this.options.$footer.html(footer);

    this.element.find('.wysihtml5').each(function() {
      $(this).cms_wysihtml5();
    });
  }
  , "{$footer} a.btn[data-toggle='modal-submit'] click" : function(el, ev) {
    var instance = this.options.instance || new this.options.model();
    var that = this;

    can.each(this.options.$content.find("form").serializeArray(), function(item) {
      instance.attr(item.name, item.value);
    });

    instance.save().done(function() {
      that.destroy().element.modal("destroy");
    }).fail(function() {

    });
  }
});

})(window.can, window.can.$);