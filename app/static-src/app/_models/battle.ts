import { Profile } from '../_models/profile';
import { Player } from '../_models/player';

export class Battle {
    id: number;
    judge: Profile;
    left: Profile;
    right: Profile;
    winner: Player;
    loser: Player;
    create_date: string;
    pick_date: string;
    expire_date: string;
}