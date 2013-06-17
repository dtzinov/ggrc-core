/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: dan@reciprocitylabs.com
 * Maintained By: dan@reciprocitylabs.com
 */

(function(can, $) {

  /* Modal Selector
   *
   * parameters:
   *   Templates:
   *     base_modal_view:
   *     option_column_view:
   *     active_column_view:
   *     option_object_view:
   *     active_object_view:
   *     option_detail_view:
   *
   *   Models and Queries:
   *     object_model: The model being linked to (the "one" in "one-to-many")
   *     option_model: The model being "selected" (the "many")
   *     option_query:
   *       Any additional parameters needed to restrict valid options
   *     active_query:
   *       Any additional parameters needed to restrict active options
   *     join_model: The model representing the join table
   *     join_query:
   *       Any additional parameters needed to restrict the join results
   *
   *   Customizable text components:
   *     modal_title:
   *     option_list_title:
   *     active_list_title:
   *     new_object_title:
   */

  can.Control("GGRC.Controllers.ModalSelector", {
    _templates: [
      "base_modal_view",
      "option_column_view",
      "active_column_view",
      "option_object_view",
      "active_object_view",
      "option_detail_view"
    ],

    defaults: {
      base_modal_view: GGRC.mustache_path + "/selectors/base_modal.mustache",
      option_column_view: GGRC.mustache_path + "/selectors/option_column.mustache",
      active_column_view: GGRC.mustache_path + "/selectors/active_column.mustache",
      option_object_view: null, //GGRC.mustache_path + "/selectors/option_object.mustache",
      active_object_view: null, //GGRC.mustache_path + "/selectors/active_object.mustache",
      option_detail_view: GGRC.mustache_path + "/selectors/option_detail.mustache",

      object_model: null,
      option_model: null,
      option_query: {},
      active_query: {},
      join_model: null,
      join_query: {},

      modal_title: null,
      option_list_title: null,
      active_list_title: null,
      new_object_title: null,
    },

    launch: function($trigger, options) {
      // Extract parameters from data attributes

      var href = $trigger.attr('data-href') || $trigger.attr('href')
        , modal_id = 'ajax-modal-' + href.replace(/[\/\?=\&#%]/g, '-').replace(/^-/, '')
        , $target = $('<div id="' + modal_id + '" class="modal modal-selector fade hide"></div>')
        ;

      $target
        .modal_form({}, $trigger)
        .ggrc_controllers_modal_selector($.extend(
          { $trigger: $trigger },
          options
        ));
    }
  }, {
    init: function() {
      var self = this
        , _data_changed = false
        ;

      this.option_list = new can.Observe.List();
      this.join_list = new can.Observe.List();
      this.active_list = new can.Observe.List();

      this.join_list.bind("change", function() {
        self.active_list.replace(
          can.map(self.join_list, function(join) {
            return new can.Observe({
              option: CMS.Models.get_instance(
                CMS.Models.get_link_type(join, self.options.option_attr),
                join[self.options.option_attr].id)
            , join: join
            });
          }))
      });

      this.join_list.bind("change", function() {
        // FIXME: This is to update the Document and Person lists when the
        //   selected items change -- that list should be Can-ified.
        var list_target = self.options.$trigger.data('list-target');
        if (list_target)
          $(list_target).tmpl_setitems(self.join_list);
      });

      this.object_model = this.get_page_model();

      $.when(
        this.post_init(),
        this.fetch_data()
      ).then(
        this.proxy('post_draw')
      );
    },

    fetch_data: function() {
      var self = this
        , join_query = {}
        ;

      join_query[this.options.join_id_field] = this.get_page_object_id();
      if (this.options.join_type_field) {
        join_query[this.options.join_type_field] = this.get_page_object_type();
      }
      $.extend(join_query, this.options.extra_join_fields);

      // FIXME: Do this better
      cache_buster = { _: Date.now() }
      return $.when(
        this.options.option_model.findAll(
          $.extend({}, this.option_query, cache_buster),
          function(options) {
            self.option_list.replace(options)
          }),
        this.options.join_model.findAll(
          $.extend({}, join_query, cache_buster),
          function(joins) {
            can.each(joins, function(join) {
              join.attr('_removed', false);
            });
            self.join_list.replace(joins);
          })
        );
    },

    post_init: function() {
      var self = this
        , deferred = $.Deferred()
        ;

      this.context = new can.Observe($.extend({
        options: this.option_list,
        joins: this.join_list,
        actives: this.active_list,
        selected: null,
      }, this.options));

      can.view(
        this.options.base_modal_view,
        this.context,
        function(frag) {
          $(self.element).html(frag);
          deferred.resolve();
          //self.post_draw();
        });

      // Start listening for events
      this.on();

      return deferred;
    },

    post_draw: function() {
      var self = this
        , $option_list = $(this.element).find('.selector-list ul')
        ;

      this.join_list.forEach(function(join, index, list) {
        $option_list
          .find('li[data-id=' + join[self.options.option_attr].id + '] input[type=checkbox]')
          .prop('checked', true);
      });
    },

    // EVENTS

    " hide": function(el, ev) {
      // FIXME: This should only happen if there has been a change.
      //   - (actually, the "Related Widget" should just be Can-ified instead)
      var list_target = this.options.$trigger.data('list-target');
      if (list_target === "refresh" && this._data_changed)
        setTimeout(can.proxy(window.location.reload, window.location), 10);
    },

    ".option_column li click": function(el, ev) {
      var option = el.data('option')
        ;

      el.closest('.modal-content').find('li').each(function() {
        $(this).removeClass('selected');
      });
      el.addClass('selected');
      this.context.attr('selected', option);
    },

    ".option_column li input[type='checkbox'] change": function(el, ev) {
      var self = this
        , option = el.closest('li').data('option')
        , join = this.find_join(option.id)
        ;

      // FIXME: This is to trigger a page refresh only when data has changed
      //   - currently only used for the Related widget (see the " hide" event)
      this._data_changed = true;

      if (el.is(':checked')) {
        // First, check if join instance already exists
        if (join) {
          // Ensure '_removed' attribute is false
          join.attr('_removed', false);
        } else {
          // Otherwise, create it
          join = this.get_new_join(option.id, option.constructor.shortName);
          join.save().then(function() {
            //join.refresh().then(function() {
              self.join_list.push(join);
            //});
          });
        }
      } else {
        // Check if instance is still selected
        if (join) {
          // Ensure '_removed' attribute is false
          if (join.isNew()) {
            // It was created, then removed, so remove from list
            join_index = this.join_list.indexOf(join);
            if (join_index >= 0) {
              this.join_list.splice(join_index, 1);
            }
          } else {
            // FIXME: The data should be updated in bulk, and only when "Save"
            //   is clicked.  Right now, it updates continuously.
            //join.attr('_removed', true);
            join.refresh().done(function() {
              join.destroy().then(function() {
                join_index = self.join_list.indexOf(join);
                if (join_index >= 0) {
                  self.join_list.splice(join_index, 1);
                }
              });
            });
          }
        }
      }
    },

    // HELPERS

    find_join: function(option_id) {
      var self = this
        ;

      return can.reduce(
        this.join_list,
        function(result, join) {
          if (result)
            return result;
          if (self.match_join(option_id, join))
            return join;
        },
        null);
    },

    match_join: function(option_id, join) {
      return join[this.options.option_id_field] == option_id ||
        (join[this.options.option_attr] 
         && join[this.options.option_attr].id == option_id)
    },

    get_new_join: function(option_id, option_type) {
      var join_params = {};
      join_params[this.options.option_id_field] = option_id;
      if (this.options.option_type_field) {
        join_params[this.options.option_type_field] = option_type;
      }
      join_params[this.options.join_id_field] = this.get_page_object_id();
      if (this.options.join_type_field) {
        join_params[this.options.join_type_field] = this.get_page_object_type();
      }
      $.extend(join_params, this.options.extra_join_fields);
      return new (this.options.join_model)(join_params);
    },

    get_page_object: function() {
      return GGRC.make_model_instance(GGRC.page_object);
    },

    get_page_model: function() {
      return this.get_page_object().constructor;
    },

    get_page_object_id: function() {
      return this.get_page_object().id;
    },

    get_page_object_type: function() {
      return this.get_page_model().shortName;
    }

  });

  function get_option_set(name) {
    // Construct options for Person and Reference selectors
    OPTION_SETS = {
      object_documents: {
        option_column_view: GGRC.mustache_path + "/documents/option_column.mustache",
        active_column_view: GGRC.mustache_path + "/documents/active_column.mustache",
        option_detail_view: GGRC.mustache_path + "/documents/option_detail.mustache",

        new_object_title: "Document",
        modal_title: "Select References",

        related_model_singular: "Document",
        related_table_plural: "documents",
        related_title_singular: "Document",
        related_title_plural: "Documents",

        option_model: CMS.Models.Document,

        join_model: CMS.Models.ObjectDocument,
        option_attr: 'document',
        join_attr: 'documentable',
        option_id_field: 'document_id',
        option_type_field: null,
        join_id_field: 'documentable_id',
        join_type_field: 'documentable_type',
      },

      object_people: {
        option_column_view: GGRC.mustache_path + "/people/option_column.mustache",
        active_column_view: GGRC.mustache_path + "/people/active_column.mustache",
        option_detail_view: GGRC.mustache_path + "/people/option_detail.mustache",

        new_object_title: "Person",
        modal_title: "Select People",

        related_model_singular: "Person",
        related_table_plural: "people",
        related_title_singular: "Person",
        related_title_plural: "People",

        option_model: CMS.Models.Person,

        join_model: CMS.Models.ObjectPerson,
        option_attr: 'person',
        join_attr: 'personable',
        option_id_field: 'person_id',
        option_type_field: null,
        join_id_field: 'personable_id',
        join_type_field: 'personable_type',
      }
    }
    return OPTION_SETS[name];
  }

  function get_relationship_option_set(data) {
    // Construct options for selectors in the Related widget
    var options = {};
    options.new_object_title = data.related_title_singular;
    options.modal_title = "Select " + data.related_title_plural;

    options.related_model_singular = data.related_model_singular;
    options.related_table_plural = data.related_table_plural;
    options.related_title_singular = data.related_title_singular;
    options.related_title_plural = data.related_title_plural;

    data.related_table_plural = 'selectors';

    option_column_view =
      GGRC.mustache_path + "/" + data.related_table_plural + "/option_column.mustache";
    active_column_view =
      GGRC.mustache_path + "/" + data.related_table_plural + "/active_column.mustache";
    option_detail_view =
      GGRC.mustache_path + "/" + data.related_table_plural + "/option_detail.mustache";

    options.option_model = CMS.Models[data.related_model];
    options.join_model = CMS.Models.Relationship;

    if (data.related_side === "destination") {
      data.object_side = "source";
    } else if (data.related_side === "source") {
      data.object_side = "destination";
    }

    options.option_attr = data.object_side;
    options.join_attr = data.related_side;
    options.option_id_field = data.object_side + "_id";
    options.option_type_field = data.object_side + "_type";
    options.join_id_field = data.related_side + "_id";
    options.join_type_field = data.related_side + "_type";

    options.extra_join_fields = {
      relationship_type_id: data.relationship_type
    };

    return options;
  }

  $(function() {
    $('body').on('click', '[data-toggle="modal-relationship-selector"]', function(e) {
      var $this = $(this)
        ;

      e.preventDefault();

      // Trigger the controller
      GGRC.Controllers.ModalSelector.launch(
        $this, get_relationship_option_set({
            related_model_singular: $this.data('related-model-singular')
          , related_title_singular: $this.data('related-title-singular')
          , related_title_plural: $this.data('related-title-plural')
          , related_table_plural: $this.data('related-table-plural')
          , related_side: $this.data('related-side')
          , related_model: $this.data('related-model')
          , relationship_type: $this.data('relationship-type')
        }));
    });
  });

  $(function() {
    $('body').on('click', '[data-toggle="modal-selector"]', function(e) {
      var $this = $(this)
        , options = $this.data('modal-selector-options')
        ;

      if (typeof(options) === "string")
        options = get_option_set(options);

      e.preventDefault();

      // Trigger the controller
      GGRC.Controllers.ModalSelector.launch($this, options);
    });
  });

})(window.can, window.can.$);
