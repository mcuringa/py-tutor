
var SocialStatus = Backbone.Model.extend({ 
  url: '/api/social/status',

});

var SocialStatusView = Backbone.View.extend({
    
    initialize: function()
    {
        this.template = _.template($('#social-status-template').html());
    },
    render: function() 
    {
        this.$el.html(this.template(this.model.attributes));
        return this;
    },

    events: 
    {
        "click #accept":  "acceptPending",
    },
    accept: function() 
    {
        var data = { "username": this.model.get("username") };
        var self = this;
        var prof = this.model;
        var updateFriend = function(data) 
        {
            prof.set(data);
            self.render();
        };

        $.ajax( {
            url: '/api/friendship/accept/',
            data: data,
            type: 'POST',
            success: updateFriend,
            error: function(data) {
                console.log('friendship acceptance failed');
                console.log(data);
            }
        });
    },

});
