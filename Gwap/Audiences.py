import Utils, json

class Audiences:

    def __init__(self, images):
        self.utils = Utils.Utils()
        self.voters = {}
        
        ## {u8: {'imgs': {img1: {d1: "description"}, img2: {d6: "description"}}, 'role':'former_voter'}, 
        ###  u9:...}
        new_describers_transformed_by_voters = self.utils.transform_former_voters_to_describers_if_img_shown_again(images)
        self.describers = new_describers_transformed_by_voters[1]
        self.init_des_id = new_describers_transformed_by_voters[0]

        self.participants = self.utils.load_participants_info()
        print('participants ' + str(json.dumps(self.participants)))
    
    def set_voters(self, voters):
        self.voters = voters
    
    def get_voters(self):
        return self.voters
    
    def set_describers(self, describers):
        self.describers = describers
    
    def get_describers(self):
        return self.describers

    def get_top_participants(self):
        top_participants = None
        if bool(self.participants):
            top_participants = sorted(self.participants.items(), key=lambda x: x[1].get("total_score"), reverse=True)
            if len(self.participants) >= 3:
                top_participants = top_participants[:3]
        
        return top_participants
    

    def refresh_players(self, images):
        new_describers_transformed_by_voters = self.utils.transform_former_voters_to_describers_if_img_shown_again(images)
        self.describers = new_describers_transformed_by_voters[1]
        self.init_des_id = new_describers_transformed_by_voters[0]
        
        self.voters = {}
    
    def get_init_des_id(self):
        return self.init_des_id

    def get_winning_des_id_foreach_img(self, img_id):
        if img_id in self.voters:
            return sorted(self.voters.get(img_id).items(), key=lambda x: len(x[1]))[-1][0]
        else:
            return None

    def is_voted_description(self, img_id, des_id):
        print("img_id " + str(img_id) + " voters " + str(json.dumps(self.voters)))
        if img_id in self.voters:
            print("let's see no vote or not " + str(json.dumps(self.voters.get(img_id).get(des_id))))
            return self.voters.get(img_id).get(des_id)
        return None

    def get_winning_des_list(self, images):
        w_des_list = []
        for img_id in images:
            winning_des_id = self.get_winning_des_id_foreach_img(img_id)
            if winning_des_id is not None:
                w_des_list.append(winning_des_id)
        
        return w_des_list
    
    def get_participants_results(self, images, game_session):

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
                        
                        prop[game_session] = {"img_w_des": {images.get(img_id): (d, 'winning')}, "role": "voter", "added_score": len(u_list)}
                        prop["total_score"] = old_score + len(u_list)
                        # prop["status"] = "rewarded"
                        prop["other_role"] = None
                        self.participants[u] = prop
        
        print("describers in get participants result " + str(json.dumps(self.describers)))
        for u, value in self.describers.items(): ## calculate or update scores for all describers who created winning descriptions this game session
            winning_d_ids = []
            no_voted_d_ids = []
            new_score = 0
            added_score = 0
            prop = {}
            imgs = value.get('imgs')
            other_role = value.get('other_role')
            
            win_or_novoted_img_desid = {} # {img1: (desid1: winning), img2: (desid2: novoted)} winning or no voted description (in case of improving description) for each image
                                            # remember each describer only gives 1 description for each image
            print("imgs in get results " + json.dumps(imgs))
            for img_id, d in imgs.items():
                d_id = next(iter(d))
                print("d_id " + d_id + " winning_des_list " + '*'.join(winning_des_list))
                if d_id in winning_des_list:
                    win_or_novoted_img_desid[images.get(img_id)] = (d_id, 'winning', len(u_list))

                    winning_d_ids.append(d_id)
                    u_list = self.voters.get(img_id).get(d_id)
                    added_score = added_score + len(u_list)
                    
                elif not self.is_voted_description(img_id, d_id) and other_role: # minus score as punishment
                                                            # for original describer and former voter 
                                                            # who created and voted for previous winning description of 
                                                            # the image was shown before but has no vote this time
                    print("punish bro ")
                    win_or_novoted_img_desid[images.get(img_id)] = (d_id, 'novoted', -1)
                    no_voted_d_ids.append(d_id)
                    
                    added_score = added_score - 1 # minus score
                    
            old_score = 0 
            if u in self.participants:
                prop = self.participants.get(u)
                old_score = prop.get("total_score")
            
            new_score = old_score + added_score
            print("win_or_novoted_img_desid " + str(json.dumps(win_or_novoted_img_desid)) + " user " + u)
            if bool(win_or_novoted_img_desid): # update only descriptions he created won or got no vote in the case of improving description
                # status = "rewarded"

                # if len(no_voted_d_ids) >= len(winning_d_ids):
                #     status = "punished"
                
                prop[game_session] = {"img_w_des": win_or_novoted_img_desid, "role": "describer", "added_score": added_score}
                prop["total_score"] = new_score
                # prop["status"] = status
                prop["other_role"] = other_role

                self.participants[u] = prop
                
        
        return self.participants