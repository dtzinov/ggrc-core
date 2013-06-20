/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all
//= require models/cacheable
(function(namespace, $){
can.Model.Cacheable("CMS.Models.Control", {
  // static properties
    root_object : "control"
  , root_collection : "controls"
  , create : "POST /api/controls"
  , update : function(id, params) {
    return $.ajax({
      url : params.selfLink
      , type : "put"
      , data : this.process_args(params, ["notes", "title", "description"])
    });
  }
  , attributes : {
    object_documents : "CMS.Models.ObjectDocument.models"
    , documents : "CMS.Models.Document.models"
    , implementing_controls : "CMS.Models.Control.models"
    , control_sections : "CMS.Models.ControlSection.models"
    //, implemented_controls : "CMS.Models.Control.models"
    //, directive : "CMS.Models.Directive.model"
    //, sections : "CMS.Models.SectionSlug.models"
  }
  // , model : function(attrs) {
  //   var id;
  //   if((id = attrs.id || (attrs[this.root_object] && attrs[this.root_object].id)) && this.findInCacheById(id)) {
  //     return this.findInCacheById(id);
  //   } else {
  //     return this._super.apply(this, arguments);
  //   }
  // }
  , defaults : {
    "type" : {id : 1}
    , "selected" : false
    , "title" : this.title || ""
    , "slug" : this.slug || ""
    , "description" : this.description || ""
  }
}
, {
// prototype properties
  init : function() {
        // This block now covered in the Cacheable model
    // if(this.control) {
    //  var attrs = this.control._attrs();
    //  for(var i in attrs) {
    //    if(attrs.hasOwnProperty(i)) {
    //      this.attr(i, this.control[i]);
    //    }
    //  }
    //  this.removeAttr("control");
    // }
    this.attr({
      "content_id" : Math.floor(Math.random() * 10000000)
    });
    this._super();
  }

  , bind_section : function(section) {
    var that = this;
    this.bind("change.section" + section.id, function(ev, attr, how, newVal, oldVal) {
      if(attr !== 'implementing_controls')
        return;

      var oldValIds = can.map(can.makeArray(oldVal), function(val) { return val.id; });

      if(how === "add" || (how === "set" && newVal.length > oldVal.length)) {
        can.each(newVal, function(el) {
          if($.inArray(el.id, oldValIds) < 0) {
            section.addElementToChildList("linked_controls", CMS.Models.Control.findInCacheById(el.id));
          }
        });
      } else {
        var lcs = section.linked_controls.slice(0);
        can.each(oldVal, function(el) {
          if($.inArray(el, newVal) < 0) {
            lcs.splice($.inArray(el, lcs), 1);
          }
        });
        section.attr(
          "linked_controls"
          , lcs
        );
      }
    });
  }
  , unbind_section : function(section) {
    this.unbind("change.section" + section.id);
  }
});

// This creates a subclass of the Control model
CMS.Models.Control("CMS.Models.ImplementedControl", {
	findAll : "GET /api/controls/{id}/implemented_controls"
}, {
});

/*
	Note: This is kind of a hack.  I would like to revisit the structure of the control models later
	in order to just pull the linked ones out of cache, but it takes some clever finagling with
	$.Deferred and it's too much work to think through at the moment.  In the meantime, implementing
	controls as a separate model from Regulation or Company controls works for my needs (comparing IDs)
	--BM 12/10/2012
*/
CMS.Models.ImplementedControl("CMS.Models.ImplementingControl", {
	findAll : "GET /api/controls/{id}/implementing_controls"
}, {});


// This creates a subclass of the Control model
CMS.Models.Control("CMS.Models.RegControl", {
	findAll : "GET /api/programs/{id}/controls"
  , attributes : {
    implementing_controls : "CMS.Models.ImplementingControl.models"
  }
	, map_ccontrol : function(params, control) {
		return can.ajax({
			url : "/mapping/map_ccontrol"
			, data : params
			, type : "post"
			, dataType : "json"
			, success : function() {
				if(control) {
					var ics;
					if(params.u) {
						//unmap
						ics = new can.Model.List();
						can.each(control.implementing_controls, function(ctl) {
              //TODO : Put removal functionality into the Cacheable, in the vein of addElementToChildList,
              //  and update this code to simply remove the unmap code.
              //We are needing to manually trigger changes in Model.List due to CanJS being unable to
              //  trigger template changes for lists automatically.
							if(ctl.id !== params.ccontrol)
							{
								ics.push(ctl);
							}
              control.attr("implementing_controls", ics);
              control.updated();
            });
          } else {
            //map
            control.addElementToChildList("implementing_controls", CMS.Models.Control.findInCacheById(params.ccontrol));
          }
				}
			}
		});
	}
}, {
	init : function() {
		this._super();
		this.attr((this.control ? "control." : "") + "type", "regulation");
	}
	, map_ccontrol : function(params) {
		return this.constructor.map_ccontrol(can.extend({}, params, {rcontrol : this.id}), this);
	}

});

})(this, can.$);
