import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SubscriberProfileFormComponent } from './subscriber-profile-form.component';

describe('SubscriberProfileFormComponent', () => {
  let component: SubscriberProfileFormComponent;
  let fixture: ComponentFixture<SubscriberProfileFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SubscriberProfileFormComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SubscriberProfileFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
