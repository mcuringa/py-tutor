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
        if(q)
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
      "change #profilePic":  "saveProfilePic",

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
        var form = this.$el.find("form")[0];
        var fields = $(form).find("input, select, textarea");
        var data = {};
        _.each(fields, function(f) {
            data[$(f).attr('name')] = $(f).val(); 
        });
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

    saveProfilePic: function() 
    {
        console.log("saving profile...");

        var picture = $('input[name="profile_pic"]')[0].files[0];
        var data = new FormData();
        data.append('file', picture);
        var self = this;
        var updateProfile = function(data) {
            console.log("profile pic uploaded");
            self.model.set("profile_pic_url", data["profile_pic_url"])
        };
        $.ajax( {
            url: '/api/profile/pic/',
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            type: 'POST',
            success: updateProfile,
            error: function(data) {
                console.log(data);
            }
        });
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
// fsv.render();

    
});
