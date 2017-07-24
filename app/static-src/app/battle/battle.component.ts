import { Component, OnInit } from '@angular/core';
import { MdIconRegistry } from '@angular/material';
import { PlayerComponent } from './player/player.component';

import { BattleService } from './battle.service';
import { Battle } from '../_models/battle';

@Component({
    selector: 'battle',
    templateUrl: './battle.component.html',
    // styleUrls: ['./battle.component.css']
})
export class BattleComponent implements OnInit {
    battles: Battle[] = [];

    constructor(private battleService: BattleService) { }
    ngOnInit() {
        // get users from secure api end point
        this.battleService.getBattles()
            .subscribe(battles => {
                this.battles = battles;
            });
    }
}
