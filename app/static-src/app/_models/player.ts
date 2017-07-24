import { Profile } from '../_models/profile';

export class Player {
    id: number;
    judge: Profile;
    target: Profile;
    mu: number;
    sigma: number;
    elo: number;
    update_date: string;
    trueskill_rank: number;
    elo_rank: number;
}