import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PlayerComponent } from './player/player.component';
import { BattleComponent } from './battle.component';

import { MaterialModule } from '@angular/material';
import { MdCardModule, MdGridListModule } from '@angular/material';
import { BattleRoutingModule } from './battle-routing.module';
import { BattleService } from './battle.service';
@NgModule({
  imports: [
    CommonModule,
    MaterialModule,
    MdCardModule,
    MdGridListModule,
    BattleRoutingModule
  ],
  declarations: [PlayerComponent, BattleComponent], 
  providers: [BattleService],
})
export class BattleModule { }
