describe("display prefs model", function() {
  
  var display_prefs;
  runs(function() {
    display_prefs = new CMS.Models.DisplayPrefs();
  });

  describe("init", function( ){

    it("sets autoupdate to true by default", function() {
      expect(display_prefs.autoupdate).toBe(true);
    });

  });

});