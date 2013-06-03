/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all
//= require models/local_storage
//= require models/display_prefs

(function(can, $){

/**
  resize_widgets_controller.js
  This controller covers the ability to resize columns (expected to the immediate children of the root element of the controller) 
  and widgets within columns (children of the column having tag name 'section' and an id attribute).  Features covered in this 
  controller are the ability to resize the columns, collapse widgets (showing only the title bar), pull widgets from the bottom
  to resize their heights with an enforced minimum, and rearrange widgets within the columns ("sorting").

*/
can.Control("CMS.Controllers.ResizeWidgets", {
  defaults : {
    columns_token : "columns"
    , heights_token : "heights"
    , total_columns : 12  //Based on bootstrap fluid rows having span1 through span12 widths
    , default_layout : null
    , page_token : null  // used for the display prefs model to determine what the defaults should be, if no record for this page exists
    , minimum_widget_height : 100 // minimum size of the *content*, or the *tab content*, of the widget
    , resizable_selector : "section[id]"  // how to determine what on the page count as widgets
    , magic_content_height_offset : 17 //10px padding of the list inside the section + 7px height of resize handle -- probably shouldn't change this
  }
}, {

  /**
    setup is a controller function that fires before the options or the events are set up.  The rationale for
    setting this.options.model in setup may not be necessary anymore but it is preserved here for legacy.
  */
  setup : function(el, opts) {
    this._super && this._super.apply(this, arguments)
    var that = this;
    CMS.Models.DisplayPrefs.findAll().done(function(data) {
      var m = data[0] || new CMS.Models.DisplayPrefs();
      m.save();
      that.options.model = m;
      that.on();
    });
  }
  
  , init : function(el, newopts) {
    this._super && this._super(newopts);
    var that = this;

    //late binding page token because the body properties are not available when the class is created
    this.options.page_token || (this.options.page_token = window.getPageToken());

    //set up dragging the bottom border to resize in jQUI
    $(this.element)
    .find(this.options.resizable_selector)
    .filter(function() {
      //don't set up resizable on collapsed widgets.  There are routines later in this file which add/remove
      // resizable functionality when the collapse state is toggled.  Also, the DashboardWidgets controller
      // handles it when new client-rendered widgets are created.  If you need to fix something about this
      // code, check those other locations as well.
      var cs = that.options.model.getCollapsed(that.options.page_token, $(this).attr("id"));
      return cs == null ? true : !cs;
    })
    .each(function() {
      //We set up minimum size based on the content or tab content height, but the resizable handle has to be
      // set on the outside widget.  So first we calculate the extra height on top of the minimum that will be,
      // meaning the height of the title bar, the height of any tabs and toolbars, and the resizer itself.
      var extra_ht = 0;
      function add_height(index, el) {
        extra_ht += $(el).height();        
      }

      $(this).children().not(".content").each(add_height);
      // look for tabs if the tabs are atop the tab content (not if they're to the left)
      if($(".content .tab-content", this).not(".tabs-left .tab-content").length) {
        $(".content .tab-content", this).siblings().each(add_height);
      }

      $(this)
      .resizable({
        handles : "s"
        , minHeight : that.options.minimum_widget_height + extra_ht
        , autoHide : false
        , alsoResize : $(this).find(".content")
      });
    });

    this.update(newopts);
  }

  /**
    if any options change, rebind event listeners and make sure the columns and heights are correct.
  */
  , update : function(newopts) {
    var that = this
    , opts = this.options;

    this.update_columns();
    this.update_heights();
    this.on();
  }

  /**
    Set up the column widths for the values stored in the display prefs.
  */
  , update_columns : function() {    
    var $c = $(this.element)
    , $children = $c.children().not(".width-selector-bar, .width-selector-drag")
    , widths = this.getWidthsForSelector($c)
    , widths
    , total_width = 0
    , that = this;


    widths = this.getWidthsForSelector($(this.element)) || [];

    for(var i = 0; i < widths.length; i++) {
      total_width += widths[i];
    }
    // Always make up the total column width with the available columns.
    //  If there is a discrepancy, try to figure out what the columns are already set to
    if(total_width != this.options.total_columns) {
      var scraped_cols = [];
      var scraped_col_total = 0;
      $children.each(function(i, child) {
        var classes = $(child).attr("class").split(" ");
        can.each(classes, function(_class) {
          var c;
          if(c = /^span(\d+)$/.exec(_class)) {
            scraped_cols.push(+c[1]);
            scraped_col_total += (+c[1]);
          }
        });
      });
    }

    if(!widths || $children.length != widths.length) {
      // In this case, widths are not set at all in the selector or the number
      //  of columns isn't what was expected from the widths collection.
      if(scraped_col_total === this.options.total_columns) {
        widths = scraped_cols;
      } else {
        // Widths are not properly set in the model AND the scraped set does not add up to the
        //  intended total, so reset to the "sensible default"
        widths = this.sensible_default($children.length);
      }
      this.options.model.setColumnWidths(this.options.page_token, $c.attr("id"), widths);
    }  

    // Get rid of previous Boostrap grid spans.
    for(i = 1; i <= this.options.total_columns; i++) {
      $children.removeClass("span" + i);
    }

    // To each child add the appropriate "span#" class for the intended width
    $children.each(function(i, child) {
      $(child).addClass("span" + widths[i]);

      // Then check whether we need to reformat the tab sheet, for any widget in the columns that has one
      can.each(
        $(child).find(that.options.resizable_selector).get()
        , that.proxy("check_horizontal_tab_sheet")
      );
    });
  }

  , " section_created" : "update_heights"

  /**
    Set the height of each visible, non-collapsed widget.  Get the heights from the display prefs
    model.  If they exist, use them; if some widgets do not have registered height, try to distribute the
    heights evenly within the viewport of the browser.

    Note that the actual heights aren't directly set on the widgets in the case that some of them aren't 
    stored in the model.  This is because saving them on the model will kick off the setting of the height
    anyway.  Doing it once at the end (the if(dirty) case) prevents infinite recursion.
  */
  , update_heights : function() {
    var model = this.options.model
    , page_heights = model.getWidgetHeights(this.options.page_token)
    , that = this
    , dirty = false
    , $c = $(this.element).children(".widget-area")
    , content_height_func = function() {
      var ch = $(this).parent().height() - parseInt($(this).parent().css("margin-bottom"));
      ch = Math.max(ch, that.options.minimum_widget_height)
      $(this).siblings().each(function() {
        ch -= $(this).height();
      });
      return ch;
    };

    if(!$c.length) {  //get whatever children the current thing has if there aren't widget area children
      $c = $(this.element).children();
    }

    $c.each(function(i, child) {
      // the grandchildren (widget descendants of the widget area) are what we'll be actually resizing
      var $gcs = $(child).find(that.options.resizable_selector);
      $gcs.each(function(j, grandchild) {
        // for a truthy value of this element's collapsed state stored in the DisplayPrefs, just collapse.
        //  Do not attempt to set size.
        if(that.options.model.getCollapsed(that.options.page_token, $(grandchild).attr("id"))) {
          $(grandchild).css("height", "").find(".widget-showhide > a").showhide("hide")
        } else {
          if(page_heights.attr($(grandchild).attr("id")) != null) {
            // case where the height for this widget is stored in the display prefs.
            var sh = page_heights.attr($(grandchild).attr("id"));
            that.set_widget_height(grandchild, sh);
          } else {
            // missing a height.  redistribute evenly but don't increase the size of anythng.
            var visible_ht = Math.floor($(window).height() - $(child).offset().top) - 10
            , split_ht = visible_ht / $gcs.length  // If you divided the visible height evenly, this is what each would get
            , col_ht = $(child).height();
            $shrink_these = $gcs.filter(function() { return $(this).height() > split_ht });  //these ones are too big
            $shrink_these.each(function(i, grandchild) {
              var $gc = $(grandchild);
              var this_split_ht = split_ht - parseInt($gc.css("margin-top")) - (parseInt($gc.prev($gcs).css("margin-bottom")) || 0);
              that.set_widget_height($gc, content_height_func.apply(grandchild));
              model.setWidgetHeight(that.options.page_token, $gc.attr("id"), this_split_ht);
              col_ht = $(child).height() + $(child).offset().top;
            });
            $gcs.not($shrink_these).each(function(i, grandchild) {  //these ones are smaller than the even split
              var $gc = $(grandchild);
              if(!page_heights.attr($gc.attr("id"))) {
                model.setWidgetHeight(that.options.page_token, $gc.attr("id"), $gc.height()); //just set these to their current
              }
            });
            //Since we've had to readjust some heights, size each widget to the new height and save to the model
            dirty = true;
            return false;
          }
        }
      });
    });
    if(dirty) {
      model.save();
      $c.find("section[id]").each(function() { that.ensure_minimum(this); });
    }
  }

  /**
    for any number of columns in the layout, return a set of column widths
    such that the innermost column (or innermost two columns for even numbers of columns) 
    gets any excess after even division.
  */
  , divide_evenly : function(n) {
    var tc = this.options.total_columns;
    var ret = [];
    while(ret.length < n) {
      ret.push(Math.floor(tc / n));
    }
    if(n % 2) {
      //odd case
      ret[Math.floor(n / 2)] += tc % (ret[0] * ret.length);
    } else {
      //even case 
      ret[n / 2 - 1] += Math.floor(tc % (ret[0] * ret.length) / 2);
      ret[n / 2] += Math.ceil(tc % (ret[0] * ret.length) / 2);
    }

    return ret;
  }

  /**
    Preferred, "aesthetically pleasing" default column widths defined here, for times when
    a default is needed.
  */
  , sensible_default : function(n) {
    var refcol;
    switch(n) {
      case 2:
      refcol = Math.floor(this.options.total_columns * 5 / 12);
      return [refcol, this.options.total_columns - refcol]; //[5,7] for default 12
      case 3:
      refcol = Math.floor(this.options.total_columns / 4); //[3,6,3] for default 12
      return [refcol, this.options.total_columns - (refcol * 2), refcol];
      default:
      return this.divide_evenly(n);
    }

  }

  /**
    Listen to changes in the DisplayPrefs model.  Using the API for DisplayPrefs, the "columns"
    are set with the id of this controller's attached element -- in all cases the parent of display
    columns. Other modifications are setting properties keyed on descendant elements' ids, not that of
    this element (explaining the first predicate below).  In short, make sure the column set is displaying
    what the model says it should be.  Same any time a height has been set -- ensure that the widget height
    matches the set height.

    We could extend this to do the same for collapse and sorts, if necessary.  Just watch out for infinite
    recursion where, e.g., setting collapse sets the model which sets the collapse.
  */
  , "{model} change" : function(el, ev, attr, how, newVal, oldVal) {
    var parts = attr.split(".");
    if(parts.length > 1 && parts[0] === window.location.pathname && parts[2] === $(this.element).attr("id")) {
      this.update_columns();
      this.options.model.save();
    }
    if(parts.length > 1 
      && parts[0] === window.location.pathname 
      && parts[1] === this.options.heights_token 
      && $(this.element).has("#" + parts[2]).length) {
      this.update_heights();
      this.options.model.save();
    }
  }

  /**
    Set the width of a column and its left sibling a fixed adjustment (an integer value such as 5 or -1).
    This first runs the adjustment through the normalizer to ensure that no column is crunched smaller than
    a width of 2 units.
    A negative adjustment value is the same as moving a dividing line to the left (the right column widens
    and the left column narrows) -- similarly, positive values move the gutter to the right.
  */
  , adjust_column : function(container, border_idx, adjustment) {
    var col = this.getWidthsForSelector(container);
    var adjustment = this.normalizeAdjustment(col, border_idx, adjustment);

    if(!adjustment)
      return;

    col.attr(border_idx, col[border_idx] - adjustment);
    col.attr(border_idx - 1, col[border_idx - 1] + adjustment);
    this.options.model.save();
  }

  /**
    Given an adjustment to make between two columns in a column layout, return the closest adjustment that
    ensures that no column is reduced to a width smaller than 2 units.
  */
  , normalizeAdjustment : function(col, border_idx, initial_adjustment) {
    var adjustment = initial_adjustment;

    if(border_idx < 1 || border_idx >= col.length) 
      return 0;

    //adjustment is +1, border_idx reduced by 1, adjustment should never be a higher number than border_idx width minus 2
    //adjustment is -1, border_idx-1 reduced by 1, adjustment should never be lower than negative( border_idx-1 width minus 2)

    adjustment = Math.min(adjustment, col[border_idx] - 2);
    adjustment = Math.max(adjustment, -col[border_idx - 1] + 2);

    return adjustment;
  }

  /**
    wrapper for DisplayPrefs column width accessor.
  */
  , getWidthsForSelector : function(sel) {
    return this.options.model.getColumnWidths(this.options.page_token, $(sel).attr("id")) || [];
  }

  /**
    given an X-offset for the whole page, return the closest column boundary (a number from 0 to options.total_columns)
    This is important when dragging around the resizer bar, because we need to know where to snap the ghost resizer to.

    This makes use of certain Bootstrap CSS magic (grid layout is done in terms of 102.5641% of the layout width), which
    explains the magic number pct_offset
  */
  , getLeftOffset : function(pageX) {
    var pct_offset = -.025641;
    var $t = $(this.element)
      , margin = parseInt($t.children('[class*=span]:last').css('margin-left'));
    return Math.round((pageX + 3 + margin / 2 - $t.offset().left) * this.options.total_columns / (1 - pct_offset) / $t.width());
  }

  /**
    Given a column boundary from 0 to options.total_columns, return the pixel offset from the left margin of the page of the
    center of the boundary (This takes into account the size of the gap between columns).
  */
  , getLeftOffsetAsPixels : function(offset) {
    var pct_offset = -.025641;
    var $t = $(this.element)
      , margin = parseInt($t.children('[class*=span]:last').css('margin-left'));
    return $t.width() * (offset / this.options.total_columns * (1 - pct_offset)) + $t.offset().left - margin / 2 - 3;
  }

  , " mousedown" : "startResize"

  /**
    Pack up the resizer bar with the data about where it started, and enable the drag mode, with the
    full opacity resizer bar and the invisible drag target that sits under the mouse pointer.

  */
  , startResize : function(el, ev) {
    var that = this;
    var origTarget = ev.originalEvent ? ev.originalEvent.target : ev.target;
    var $t = $(this.element);
    //Don't start drag if you're not over a gutter (not clicking directly on the parent of the columns
    // or the resizer bar, not currently showing the bar)
    if (($t.is(origTarget) || $(origTarget).is(".width-selector-bar, .width-selector-drag"))
        && $(".width-selector-bar", $t).length) {
      var offset = this.getLeftOffset(ev.pageX);
      var widths = that.getWidthsForSelector($t).slice(0);
      var c_width = that.options.total_columns;
      while(c_width > offset) { //should be >=?
        c_width -= widths.pop();
      }
      //create the bar that shows where the new split will be, if it doesn't exist
      //  (really it should have been created already for the ghost bar)
      var $bar = $(".width-selector-bar", $t);
      if(!$bar.length) {
        $bar = $("<div>&nbsp;</div>")
        .addClass("width-selector-bar")
        .data("offset", offset)
        .data("start_offset", offset)
        .data("index", widths.length)
        .css({
          width: "5px"
          , height : $t.height()
          , position : "fixed"
          , left : this.getLeftOffsetAsPixels(offset)
          , top : $t.offset().top - $(window).scrollTop()
        }).appendTo($t);
      }
      $bar.css("opacity", "1.0");
      //create an invisible drag target so we don't drag around a ghost of the bar
      $("<div>&nbsp;</div>")
      .attr("draggable", true)
      .addClass("width-selector-drag")
      .css({
        left : ev.pageX - $(window).scrollLeft() - 1
        , top : ev.pageY - $(window).scrollTop() - 1
        , position : "fixed"
        , width : "3px"
        , height : "3px"
        , cursor : "move"
      })
      .appendTo($t);
    }
  }

  /**
    on these events, check whether we should show the resize bar in the gutter between two columns
  */
  , " mouseover" : "showGhostResizer"
  , " mousemove" : "showGhostResizer"
  , "{window} resize" : function(el, ev) {
    var that = this;
    this.showGhostResizer(this.element, ev);
    this.element.find(this.options.resizable_selector).filter(":has(.content:visible)").each(function(i, el) {
      that.ensure_minimum(el);
      that.check_horizontal_tab_sheet(el);
    });
  }


  /**
    When moused over the gutter between two widgets, show a half-opacity resizer bar.
  */
  , showGhostResizer : function(el, ev) {
    var that = this;
    var origTarget = ev.originalEvent ? ev.originalEvent.target : ev.target;  //what did we actually mouse over?
    var $t = $(this.element);
    // First test -- don't show resizer if we are not directly over the content box (outside any column), and not over the 
    //  resizer bar, and the drag box doesn't exist (because we're not dragging).
    if(!$t.is(origTarget) && !$(origTarget).is(".width-selector-bar") && !$(".width-selector-drag", $t).length ) {
      this.removeResizer();
      return;
    }
    var offset = this.getLeftOffset(ev.pageX);
    var widths = this.getWidthsForSelector($t).slice(0);
    var acc = 0;
    //Second test:  don't show resizer if we are outside of the gutters between colunns (probably below the content of a column)
    for(var i = 0; i < widths.length && acc !== offset; i++) {
      acc += widths[i];
      if(acc > offset) { //counted past our current offset. we're not near a gutter.
        this.removeResizer();
        return;
      }
    }

    var gutterX = this.getLeftOffsetAsPixels(offset);
    var gutterWidth = Math.max.apply(Math, $t.children().map(function() { return parseInt($(this).css("margin-left")); }).get());

    // If a resizer bar doesn't exist and we're in a gutter...
    if (!$(".width-selector-bar, .width-selector-drag").length
      && Math.abs(ev.pageX - gutterX) < gutterWidth / 2) {
      var c_width = that.options.total_columns;
      while(c_width > offset) { //should be >=?
        c_width -= widths.pop();
      }
      //...create the bar that shows where the new split will be
      $("<div>&nbsp;</div>")
      .addClass("width-selector-bar")
      .data("offset", offset)
      .data("start_offset", offset)
      .data("index", widths.length)
      .css({
        width: "5px"
        , height : $t.height()
        , position : "fixed"
        , left : gutterX
        , top : $t.offset().top - $(window).scrollTop()
        , opacity : "0.5"
      }).appendTo($t);
    }
  }

  /**
    After dragging the resizer drag element around (not the resizer bar but the little draggable box
     we put under the pointer), find out where we dropped it and adjust the relevant columns as necessary
  */
  , completeResize : function(el, ev) {
    var $drag = $(".width-selector-drag");
    if($drag.length) { // only do this if we have been dragging around the drag selector.  Note that this
                       // has to change if browser compatibility makes us draw the drag box before dragging.
                       // (a possibility since the code we have right now doesn't work in Firefox)
      var that = this
      , t = this.element
      , $bar = $(".width-selector-bar")
      , offset = $bar.data("offset")
      , start_offset = $bar.data("start_offset") // this was set up when we started dragging
      , index = $bar.data("index");

      this.adjust_column(t, index, offset - start_offset);
      $(".width-selector-drag", t).remove();
      $(".width-selector-bar", t).css("opacity", "0.5") //"Ghost" the resizer bar
      if(!$(document.elementFromPoint(ev.pageX, ev.pageY)).is($(t).add(".width-selector-bar"))) {
        //currently outside the gutter after dropping.  remove the ghost resizer.
        this.removeResizer();
      }
      t.find(this.options.resizable_selector).each(function(i, section) {
        that.ensure_minimum(section);
        that.check_horizontal_tab_sheet(section);
      });
    }

  }

  /**
    Remove the resizer bar.  This happens mostly when the pointer leaves the gutter between widgets.
  */
  , removeResizer : function(el, ev) {    
    $(".width-selector-bar", this.element).remove();
  }

  /**
    Whichever of mouseup or dragend happens, call the completeResize function.
  */
  , " mouseup" : "completeResize"
  , " dragend" : "completeResize"

  , " dragover" : "recalculateDrag"
  , recalculateDrag : function(el, ev) {
    var $drag = $(this.element).find(".width-selector-drag");
    var $bar =  $(this.element).find(".width-selector-bar")
    if($drag.length) {
      var $t = $(this.element)
      , offset = this.getLeftOffset(ev.pageX)
      , adjustment = this.normalizeAdjustment(this.getWidthsForSelector($t), $bar.data("index"), offset - $bar.data("start_offset"));

      offset = $bar.data("start_offset") + adjustment;

      $bar
      .data("offset", offset)
      .css("left", this.getLeftOffsetAsPixels(offset));
      ev.preventDefault();
    }
  }

  /**
    jQUI event, when the user stops dragging the resize handle in a widget.
  */
  , " resizestop" : function(el, ev, ui) {
    var ht = $(ui.element).height();
    this.ensure_minimum($(ui.element).closest(this.options.resizable_selector), ht);
  }

  /**
    Synthetic event that allows other controllers, like DashboardWidgets, to indicate to this controller that it
    should set minimum height, e.g. for a widget that was just created.
  */
  , "{resizable_selector} min_size" : function(el, ev) {
    this.ensure_minimum(el);
  }

  /**
    set the height of a widget to the supplied height, or to the minimum height established in
    the controller instance options, whichever is greater.  The height minimum is calculated against the 
    "content" section, but the resizing is applied to the widget section. This function calculates the
    difference between the two and acts accordingly
  */
  , ensure_minimum : function(el, ht) {
    var $el = $(el);
    $el.css("width", "").find(".content").css("width", ""); //bizarre jQUI behavior fix
    if(!$el.find(".widget-showhide .active").length) {
      return; //don't resize widgets that are collapsed
    }

    if(!ht) {
      ht = $el.height();  //height not supplied just means to check the widget's current height against the minimum
    }

    var min_ht = this.options.minimum_widget_height;
    function add_height(index, elt) {
      min_ht += $(elt).height();
    }

    // To calculate the delta between the intended content height and the intended widget height, add all of the
    //  heights of the content's siblings. 
    $el.children().not(".content, .ui-resizable-handle").each(add_height);
    // If the content is a tab sheet, also add the height of the tabs and any button barse.
    if($(".content .tab-content", el).not(".tabs-left .tab-content").length) {
      $(".content .tab-content", el).siblings().each(add_height);
    }

    //Enable/re-enable resizable if it's not currently set up.
    if($el.is(":not(.ui-resizable)") || $el.resizable("option").minHeight !== min_ht) {
      if($el.is(".ui-resizable")) {
        $el.resizable("destroy");
      }
      $el.resizable({
        handles : "s"
        , minHeight : min_ht
        , autoHide : false
        , alsoResize : $el.find(".content")
      });
    }
    if(ht < min_ht) {
      ht = min_ht;
    }
    this.set_widget_height(el, ht);
    this.options.model.setWidgetHeight(this.options.page_token, $el.attr("id"), ht);
  }

  /**
    lower-level function than ensure_minimum
    sets the height of the widget and its associated content pane
  */
  , set_widget_height : function(el, ht) {
    var $el = $(el);
    $el.css("height", ht);

    // The remainder of this method determines what the height of the content should be set to.
    var content_ht = ht;
    var min_content_ht = this.options.minimum_widget_height;
    function add_height_outside(index, elt) {
      content_ht -= $(elt).height();
    }
    function add_height_inside(index, elt) {
      min_content_ht += $(elt).height();
    }

    // "outside" height is for the siblings of the content section, and gets subtracted
    //  from the content section height.
    $el.children().not(".content, .ui-resizable-handle").each(add_height_outside);
    // "inside" height is for the siblings of the tab pane, if there is a top-arranged tab sheet,
    //  and gets added to the content *minimum* height
    if($(".content .tab-content", el).not(".tabs-left .tab-content").length) {
      $(".content .tab-content", el).siblings().each(add_height_inside);
    }

    $el.find(".content:first").css("height", Math.max(min_content_ht, content_ht) - this.options.magic_content_height_offset);
  }

  /**
    Where we have horizontal tab sheets in the resizable columns, it's a bit more aesthetic to not stack them
    into multiple rows when possible.  If we can avoid this by removing the text from the tabs and making the 
    a
  */
  , check_horizontal_tab_sheet : function(el) {
    var $el = $(el);
    $el = $el.is(".nav-tabs:not(.tabs-left > *)") ? $el.first() : $el.find(".nav-tabs:not(.tabs-left > *):first");

    if(!$el.length)
      return;

    $el.find("a:data(text)").each(function(i, tablink) {
      var $tab = $(tablink);
      $tab.append($tab.data("text")).tooltip("disable").removeData("text");
    });

    var fullwidth = can.reduce($el.children(), function(total, t) {
      return total + $(t).width();
    }, 0);

    if(fullwidth > $el.parent().width()) {
      //this is where we need to shrink
      $el.find("a:not(:data(text))").each(function(i, tablink) {
        var $tab = $(tablink)
        , oldtmpl = $tab.attr("data-template");
        $tab
        .data("text", $tab.text())
        .attr("data-original-title", $tab.text())
        .removeAttr("data-template")
        .tooltip({delay : {show : 500, hide : 0}})
        .tooltip("enable")
        .html($tab.children())
        .attr("data-template", oldtmpl);
      });
    }
  }

  /**
    Classic Mac-style windowshading.  Double-click on title bar collapses the widget
  */
  , "section[id] > header dblclick" : function(el, ev) {
    if(!$(ev.target).closest(".widget-showhide").length) {
      $(el).find(".widget-showhide a").click();
    }
  }

  /**
    Widget collapse handler.  This turns off the resizing when in the collapsed state,
    and sets the state on the DisplayPrefs.  when the widget is uncollapsed, the last known
    height of the widget or the minimum widget height is restored, whichever is larger, and
    reinitializes resizable.
  */
  , ".widget-showhide click" : function(el, ev) {
    var that = this;
    //animation hasn't completed yet, so collapse state is inverse of whether it's actually collapsed right now.
    var $section = el.closest(this.options.resizable_selector);
    var collapse = $section.find(".content").is(":visible");
    collapse && $section.css("height", "").find(".content").css("height", "");
    if(collapse && $section.is(".ui-resizable")) {
      $section.resizable("destroy");
    } else if(!collapse) {
      setTimeout(function() { 
        that.ensure_minimum($section, that.options.model.getWidgetHeight(that.options.page_token, $section.attr("id")));
      }, 1);
    }
    that.options.model.setCollapsed(that.options.page_token, $section.attr("id"), collapse);
  }

});

})(this.can, this.can.$);