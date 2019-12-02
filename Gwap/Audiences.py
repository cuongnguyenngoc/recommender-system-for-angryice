import Utils, json

class Audiences:

    def __init__(self, images):
        self.utils = Utils.Utils()
        self.voters = {}
        
        tmp = self.utils.get_old_participants_for_used_images(images)
        self.old_participants = tmp[0]
        self.init_des_id = tmp[1]
        self.descriptions = tmp[2]

        ## {u8: {'imgs': {img1: {d1: "description"}, img2: {d6: "description"}}, 'role':'former_voter'}, 
        ###  u9:...}
        self.describers = {}

        self.participants = self.utils.load_participants_info()
        # print('participants ' + str(json.dumps(self.participants)))
    
    def set_voters(self, voters):
        self.voters = voters
    
    def get_voters(self):
        return self.voters
    
    def set_describers(self, describers):
        self.describers = describers
    
    def get_describers(self):
        return self.describers

    def get_old_participants(self):
        return self.old_participants
    
    def get_top_participants(self):
        top_participants = None
        if bool(self.participants):
            top_participants = sorted(self.participants.items(), key=lambda x: x[1].get("total_score"), reverse=True)
            if len(self.participants) >= 3:
                top_participants = top_participants[:3]
        
        return top_participants
    

    def refresh_players(self, images):
        tmp = self.utils.get_old_participants_for_used_images(images)
        self.old_participants = tmp[0]
        self.init_des_id = tmp[1]
        self.descriptions = tmp[2]
        
        self.describers = {}
        self.voters = {}
    
    def get_descriptions(self):
        return self.descriptions
    
    def get_init_des_id(self):
        return self.init_des_id

    def get_winning_des_id_foreach_img(self, img_id):
        if img_id in self.voters:
            return sorted(self.voters.get(img_id).items(), key=lambda x: len(x[1]))[-1][0]
        else:
            return None

    def get_winning_des_list(self, images):
        w_des_list = []
        for img_id in images:
            winning_des_id = self.get_winning_des_id_foreach_img(img_id)
            if winning_des_id is not None:
                w_des_list.append(winning_des_id)
        
        return w_des_list
    
    def get_participants_results(self, images, game_session, descriptions):

        # if bool(self.voters): # do all this when voters do something, means there is some winning description
        winning_des_list = self.get_winning_des_list(images)

        for img_id, des_list in self.voters.items(): ## calculate or update scores for all voters who voted winning descriptions this game session
            for d, u_list in des_list.items():
                if d in winning_des_list:
                    for u in u_list:
                        old_score = 0
                        prop = {}
                        if u in self.participants:
                            prop = self.participants.get(u)
                            old_score = prop.get("total_score")
                        
                        prop[game_session] = {"role": "voter", "added_score": len(u_list)}
                        prop["total_score"] = old_score + len(u_list)

                        self.participants[u] = prop
                        self.utils.store_winning_user(u, game_session, images.get(img_id), descriptions.get(d)[1], "voter")
        
        print("describers in get participants result " + str(json.dumps(self.describers)))
        for u, imgs in self.describers.items(): ## calculate or update scores for all describers who created winning descriptions this game session
            new_score = 0
            added_score = 0
            prop = {}
            
            print("imgs in get results " + json.dumps(imgs))
            for img_id, d in imgs.items():
                d_id = next(iter(d))
                
                if d_id in winning_des_list:
                    u_list = self.voters.get(img_id).get(d_id)
                    added_score = added_score + len(u_list)
                    self.utils.store_winning_user(u, game_session, images.get(img_id), descriptions.get(d_id)[1], "describer")
                    
            old_score = 0 
            if u in self.participants:
                prop = self.participants.get(u)
                old_score = prop.get("total_score")
            
            if added_score > 0:
                new_score = old_score + added_score
                prop[game_session] = {"role": "describer", "added_score": added_score}
                prop["total_score"] = new_score

                self.participants[u] = prop
        
        for u, value in self.old_participants.items():
            if value.get("des_id") not in winning_des_list:
                added_score = -1
                old_score = 0
                new_score = 0
                role = value.get("other_role")
                prop = {}
                if u in self.participants:
                    prop = self.participants.get(u)
                    old_score = prop.get("total_score")
                    new_score = old_score + added_score
                    if game_session in prop:
                        added_score = prop.get(game_session).get("added_score") - added_score
                        role = prop.get(game_session).get("role")
                prop[game_session] = {"role": role, "added_score": added_score}
                prop["total_score"] = new_score
                self.participants[u] = prop

        return self.participants