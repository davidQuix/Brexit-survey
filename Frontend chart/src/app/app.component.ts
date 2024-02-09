import { Component, OnInit } from '@angular/core';
import { MediaObserver } from '@angular/flex-layout';
import { ConnectionStatus, QuixService } from './services/quix.service';
import { ParameterData } from './models';
import { Observable, map } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  workspaceId: string;
  values$: Observable<{ [key: string]: number[] }>

  constructor(private quixService: QuixService) { }

  ngOnInit(): void {
    this.values$ = this.quixService.paramDataReceived$.pipe(map((m) => m.numericValues));

    this.values$.subscribe((values) => {
      console.log(values)
    })

    this.quixService.readerConnStatusChanged$.subscribe((status) => {
      if (status !== ConnectionStatus.Connected) return;
      this.workspaceId = this.quixService.workspaceId;
      const topicId = this.quixService.workspaceId + '-' + this.quixService.chartDataTopic;
      this.quixService.subscribeToParameter(topicId, '*', '*');
    });
  }
}
