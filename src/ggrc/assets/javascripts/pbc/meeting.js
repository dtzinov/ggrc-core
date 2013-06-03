/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all
//= require models/cacheable

can.Model.Cacheable("CMS.Models.Meeting", {
  destroy : "DELETE /meetings/{id}.json"
}, {
  init : function () {
      this._super && this._super();
      // this.bind("change", function(ev, attr, how, newVal, oldVal) {
      //     var obj;
      //     if(obj = CMS.Models.ObjectDocument.findInCacheById(this.id) && attr !== "id") {
      //         obj.attr(attr, newVal);
      //     }
      // });

      var that = this;

      this.each(function(value, name) {
        if (value === null)
          that.removeAttr(name);
      });
  }

});