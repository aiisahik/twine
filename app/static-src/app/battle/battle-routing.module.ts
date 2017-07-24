import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BattleComponent } from './battle.component';
import { PlayerComponent } from './player/player.component';

const battleRoutes: Routes = [
  {
    path: '',
    component: BattleComponent,
    children: [
        {
            path: 'player/:id',
            component: PlayerComponent,
        }
    ] 
  },
];

@NgModule({
  imports: [
    RouterModule.forChild(
      battleRoutes,
    )
  ],
  exports: [
    RouterModule
  ],
  // providers: [
  //   CanDeactivateGuard,
  //   SelectivePreloadingStrategy
  // ]
})

export class BattleRoutingModule { }