import { Component, OnInit } from '@angular/core';
import { MediaObserver } from '@angular/flex-layout';
import { ConnectionStatus, QuixService } from './services/quix.service';
import { ParameterData } from './models';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  workspaceId: string;

  constructor(private quixService: QuixService, public media: MediaObserver) { }

  ngOnInit(): void {
    this.quixService.paramDataReceived$.subscribe((parameter: ParameterData) => {
      console.log(parameter)
    });

    this.quixService.readerConnStatusChanged$.subscribe((status) => {
      if (status !== ConnectionStatus.Connected) return;
      this.workspaceId = this.quixService.workspaceId;
      const topicId = this.quixService.workspaceId + '-' + this.quixService.chartDataTopic;
      this.quixService.subscribeToParameter(topicId, '*', 'Support');
    });
  }
}
