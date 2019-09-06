
class Audiences:

    def __init__(self):
        self.voters = {}
        self.describers = {} ### {u8: {img1: {d1: "description"}, img2: {d6: "description"}}, u9:...}
        self.participants = {} ### {img1: {d1: [u1, u2, u3], d2: [u4, u5]}, img2:...}
    
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
    

    def refresh_players(self):
        self.describers = {}
        self.voters = {}
    
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
    
    def get_participants_results(self, images, game_session):

        if bool(self.voters): # do all this when voters do something, means there is some winning description
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
                            
                            prop[game_session] = {"img": images.get(img_id), "des_ids": [d], "role": "voter", "added_score": len(u_list)}
                            prop["total_score"] = old_score + len(u_list)
                            self.participants[u] = prop
            
            for u, imgs in self.describers.items(): ## calculate or update scores for all describers who created winning descriptions this game session
                d_ids = []
                new_score = 0
                added_score = 0
                prop = {}
                for img_id, d in imgs.items():
                    d_id = next(iter(d))
                    if d_id in winning_des_list:
                        d_ids.append(d_id)
                        u_list = self.voters.get(img_id).get(d_id)
                        added_score = len(u_list)
                        old_score = 0
                        if u in self.participants:
                            prop = self.participants.get(u)
                            old_score = prop.get("total_score")
                        new_score = old_score + added_score
                if d_ids and new_score > 0: # update only descriptions he created won
                    prop[game_session] = {"img": images.get(img_id), "des_ids": d_ids, "role": "describer", "added_score": added_score}
                    prop["total_score"] = new_score
                    self.participants[u] = prop
        
        return self.participants