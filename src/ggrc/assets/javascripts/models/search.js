can.Model("GGRC.Models.Search", {

  findOne : "GET /search"
  , search : function(str, params) {
    return this.findOne($.extend({q : str}, params));
  }
  , init : function() {
    this._super && this._super.apply(this, arguments);
    var _findOne = this.findOne;
    this.findOne = function() {
      return _findOne.apply(this, arguments).then(function(data) {
        data.attr("entries", data.results.entries);
        data.removeAttr("results");
        return data;
      });
    };
  }
}, {

  getResultsFor : function(type) {
    var _class = type.shortName
      ? type
      : (can.getObject("CMS.Models." + type) || can.getObject("GGRC.Models." + type));

    type = _class.shortName;
    return can.map(
      this.entries
      , function(v) {
        var inst;
        if(v.type === type) {
          inst = new _class({id : v.id});
          // if(!inst.selfLink) {
          //   inst.attr("selfLink", v.href);
          //   inst.refresh();
          // }
          return inst;
        }
    });
  }

});