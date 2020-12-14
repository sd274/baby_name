console.log('file loaded')

function titleCase(string) {
    var sentence = string.toLowerCase().split(" ");
    for (var i = 0; i < sentence.length; i++) {
        sentence[i] = sentence[i][0].toUpperCase() + sentence[i].slice(1);
    }
    sentence = sentence.join(" ");
    return sentence;
}


BabyName = function (_target_div, _user_id) {

    var self = this;
    self.target_div = _target_div;
    self.user_id = _user_id;
    self.sex = 'boy';

    self.prepare_div = function () {
        $(self.target_div).empty();
        $(self.target_div).append(
            `
            <div id='dispaly_names'></div>
            <div id='reaction_buttons'></div>
            <div id='add_baby_name_div'></div>
            <div id='display_reaction_buttons' class=''></div>
            <div id='display_reactions' class = 'name-card-container'></div>
           
            `
        );
        self.display_name_div = self.target_div + ' #dispaly_names';
        self.reaction_buttons_div = self.target_div + ' #reaction_buttons';
        self.display_reaction_buttons_div = self.target_div + ' #display_reaction_buttons';
        self.display_reactions_div = self.target_div + ' #display_reactions';
        self.add_baby_name_div = self.target_div + ' #add_baby_name_div';

    }

    self.send_reaction = function (babyNameId, reactionId) {
        var query = `
        mutation react {
            userReaction(input:{babyNameId:$babyNameId$,reactionId:$reactionId$}){
              ok
              userNameReaction{
                id
                name{id name}
                reaction{id reaction}
                
              }
            }
          }
          `
        query = query
            .replace('$babyNameId$', babyNameId)
            .replace('$reactionId$', reactionId)
        $.ajax({
            url: graphql_url,
            contentType: "application/json",
            type: "POST",
            data: JSON.stringify({
                query: query
            }),
            success: function (result) {
                self.current_reaction_id = reactionId;
                var reaction_data = result.data.userReaction.userNameReaction;
                self.update_page_reactions(reaction_data)
                self.display_user_reactions(reactionId);
                self.display_name();
            }
        })

    }


    self.prep_recs = function (babyNameId, reactionId) {
        var query = `
        query prepCluster {
            prepCluster 
          }
          `

        $.ajax({
            url: graphql_url,
            contentType: "application/json",
            type: "POST",
            data: JSON.stringify({
                query: query
            }),
            success: function (result) {
                console.log(result);
            }
        })

    }

    

    self.get_user_reactions = function (reaction_id) {
        var query = `
        query userReactions {
            userReactions {
              id
              name{
                id
                name
              }
              reaction{
                id
                reaction
              }
            }
          }
        `

        $.ajax({
            url: graphql_url,
            contentType: "application/json",
            type: "POST",
            data: JSON.stringify({
                query: query
            }),
            success: function (result) {
                console.log(result);
                self.user_name_reactions = result.data.userReactions;
            }
        })
    }

    self.update_page_reactions = function (reaction_data) {
        // update the reactions stored in the browser
        self.user_name_reactions.push(reaction_data);
    }





    self.display_user_reactions = function (reaction_id) {
        var to_append = "<div class='reaction-container'>";
        var userReactions = self
            .user_name_reactions
            .filter(
                x => (x.reaction.id == reaction_id)
            );

        self.current_user_reactions = [];
        userReactions.forEach(reaction => {
            var appending = "<div id='reaction-$id$' class='reaction-item'><h4>$name$</h4></div>"
            appending = appending.replace('$name$', titleCase(reaction.name.name));
            appending = appending.replace('$id$', reaction.id)
            to_append += appending;
            self.current_user_reactions.push(reaction.id)
        })
        to_append += '</div>';
        $(self.display_reactions_div).empty();
        $(self.display_reactions_div).append(to_append);
    }

    

    self.add_ractions = function () {
        var query = `
        query reactions{
            reactions{
              id
              reaction
            }
          }
        `

        self.reaction_buttons = [];

        $.ajax({
            url: graphql_url,
            contentType: "application/json",
            type: "POST",
            data: JSON.stringify({
                query: query
            }),
            success: function (result) {
                self.reactions = result.data.reactions;
                var to_append = "<div class='reaction_button_div'>";
                self.reactions.forEach(element => {
                    var appending = "<button class='reaction-button' id='$reaction_id$' value='$reaction$'>$reaction$</button>"
                    appending = appending
                        .replace('$reaction$', element.reaction)
                        .replace('$reaction$', element.reaction)
                        .replace('$reaction_id$', element.id);
                    to_append += appending;
                });
                to_append += '</div>'
                $(self.reaction_buttons_div).append(to_append);
                $(self.display_reaction_buttons_div).append('<h1> See Your Previous Reactions</h1>' + to_append);
                self.reactions.forEach(element => {
                    var button_id = self.reaction_buttons_div + ' #' + element.id;
                    $(button_id).click(_ => {
                        self.send_reaction(self.current_name_id, element.id);
                    })

                    var reaction_button_id = self.display_reaction_buttons_div + ' #' + element.id;
                    $(reaction_button_id).click(_ => {
                        self.current_reaction_id = element.id;
                        self.display_user_reactions(element.id);
                    })
                })
            }
        })
    }






    self.display_name = function () {
        var query = `
        query nameRecommendation {
            nameRecommendation(sex:"$sex$"){
              id	
              sex
              name
            }
          }
        `

        query = query
            .replace('$sex$', self.sex);
        $.ajax({
            url: graphql_url,
            contentType: "application/json",
            type: "POST",
            data: JSON.stringify({
                query: query
            }),
            success: function (result) {
                var div = self.display_name_div;
                $(div).empty();
                var name = result.data.nameRecommendation;
                self.current_name_id = name.id;
                var to_append = "<h2>What do you think of?</h1>"
                to_append += "<div class='display_baby_name_div'><h1>" + titleCase(name.name) + "</h1></div>"
                $(div).append(to_append);
            }
        })
    }




    self.prepare_div();
    self.add_ractions();
    self.user_name_reactions = self.get_user_reactions();
}