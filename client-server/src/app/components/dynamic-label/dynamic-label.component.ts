import { Component, OnInit, Output, Input, EventEmitter, DoCheck, KeyValueDiffers, KeyValueDiffer } from '@angular/core';

@Component({
  selector: 'app-dynamic-label',
  templateUrl: './dynamic-label.component.html',
  styleUrls: ['./dynamic-label.component.scss']
})
export class DynamicLabelComponent implements OnInit {
  @Input() name: string;
  @Input() message: string;
  open: boolean = false;
  differ: KeyValueDiffer<string,any>;

  constructor(private differs: KeyValueDiffers) {
      this.differ = this.differs.find({}).create();
   }

  ngOnInit(): void { }

  //checks changes to the field to modify its open/closed state 
  ngDoCheck(){
      const change = this.differ.diff(this);
      if(change){
          change.forEachChangedItem(item => {
              if(item.key == 'message'){
                  this.open = item.currentValue.toString() == '' ;
              }
          });
      }
  }

}
