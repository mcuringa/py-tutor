$("body").ready(function() 
{



var SocialProfile = Backbone.Model.extend({ 
    url:"/api/profile/", 
});

// var Message = Backbone.Model.extend();
var Friend = Backbone.Model.extend({ urlRoot : '/api/friends', });
var Friends = Backbone.Collection.extend({
    model: Friend,
    url: '/api/friend/find',
});

var SearchResultView = Backbone.View.extend({
    template: _.template($('#friend-result-tmpl').html()),
    
    render: function() 
    {
        console.log("rendering result");
        console.log(this.model.username);
        
        this.$el.html(this.template(this.model.attributes));
        return this;
    },
});

var FriendSearchView = Backbone.View.extend({
    
    template: _.template($('#friend-search-tmpl').html()),

    initialize: function() 
    {
         this.listenTo(this.collection, "reset", this.renderResults);
    },

    events: 
    {
        "keyup #search-field":  "search",
    },

    search: function()
    {
        var q = $("#search-field").val();
        if(q && q.length > 2)
        {
            this.collection.fetch({ 
                reset: true, 
                data: { q: q},
            });
        }
    },

    renderResult: function(friend) 
    {
      var view = new SearchResultView({model: friend});
      this.$("#search-results").append(view.render().el);
    },

    renderResults: function() 
    {
        console.log('rendering search results');
        console.log(this.collection.toJSON());
        $("#search-results").empty();
        this.collection.each(this.renderResult, this);
        return this;
    },

    render: function() 
    {
        this.$el.html(this.template({}));
        return this;
    }


});



var ProfileFormView = Backbone.View.extend({
    
    template: _.template($('#profile-form-tmpl').html()),

    initialize: function() 
    {
        this.updateBioChars();
        this.listenTo(this.model, 'change', this.render);
    },
    
    isDirty: false,
    lastKey: -1,
    lastSync: 0,
    syncDelay: 2000,
    syncLock: false,

    events: 
    {
      "keyup #bio":  "updateBioChars",
      "keyup #profile-form .form-control":  "dirty",

    },

    dirty: function(e)
    {
        this.lastKey = _.now();
        this.isDirty = true;
        if(!this.syncLock)
            this.syncToServer()

    },

    updateModel: function()
    {
        var form = this.$el.children("form")[0];
        var fields = $(form).find("input, select, textarea");
        var data = {};
        _.each(fields, function(f) {
            data[$(f).attr('name')] = $(f).val(); 
        });
        // console.log(data);
        this.model.set(data);
    },

    syncToServer: function()
    {
        var delta = _.now() - this.lastKey;
        if(this.isDirty && delta > this.syncDelay)
        {
            this.updateModel();

            // this.model.save({ headers: {'X-CSRFToken': this.csrftoken} });           
            this.model.save();

            this.isDirty = false;
            this.syncLock = false;

        }
        else
        {
            var self = this;
            var syncAfterDelta = function(){ self.syncToServer(); };
            window.setTimeout(syncAfterDelta, this.syncDelay);            
        }

    },

    updateBioChars: function()
    {
        var bio = $("#bio").val();
        if(bio)
            $("#bio_chars_left").html(200 - bio.length );
        
    },

    render: function() {
        this.$el.html(this.template(this.model.attributes));
        this.updateBioChars();
        return this;
    }
});




var csrftoken = $.cookie('csrftoken');
var profile = new SocialProfile();
profile.fetch();

var pfv = new ProfileFormView({el: "#profile", model: profile, csrftoken: csrftoken});

var friends = new Friends();

var searchResults = new Friends();

var fsv = new FriendSearchView( {el: "#friend-search", collection: searchResults } );
fsv.render();

    
});
