/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require controls/control
//= require controls/controls_controller
(function(namespace, $) {

// Explicitly short circuit until handling of implemented/implementing controls
// is complete.
return;

if (!/\/controls/.test(window.location.pathname))
  return;

var controlId = namespace.location.pathname.substr(window.location.pathname.lastIndexOf("/") + 1);

$(function() {
	// The following uncommented line is equivalent to doing its preceding commented line, but we have a jQuery CanJS helpers option added:
    //CMS.Controllers.Controls.Instances = { Control : new CMS.Controllers.Controls('#controls', { arity : 2 })};
    CMS.Controllers.Controls.Instances = {
    	Control : $("#controls").cms_controllers_controls({
    		arity : 2
    		, id : controlId
    		, model : (/^\d+$/.test(controlId) ? CMS.Models.ImplementedControl : CMS.Models.Control)
    		, list : "/static/mustache/controls/tree.mustache"
    	}).control(CMS.Controllers.Controls)};
});

})(this, jQuery);
