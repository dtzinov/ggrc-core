/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require products/routes_controller
(function(namespace, $) {

// Explicitly short circuit until handling of implemented/implementing controls
// is complete.

if (!/\/products/.test(window.location.pathname))
  return;

$(function() {
    CMS.Controllers.DirectiveRoutes.Instances = {
      Control : $(document.body).cms_controllers_product_routes({}).control(CMS.Controllers.ProductRoutes)};
});

})(this, jQuery);
