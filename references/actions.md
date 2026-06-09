# Shortcuts Actions Reference

Reference for WF*Action identifiers and sample-verified modern action identifiers.

The base catalog came from WF*Action names. The "Production Sample Verified" section below is updated from three current exported shortcuts: Momo, Vector Config, and Vector. Treat sample-verified identifiers as authoritative when they conflict with older inferred names.

## Identifier Mapping Rules

### Standard Mapping
Class `WF<Name>Action` maps to `is.workflow.actions.<lowercasename>`

Example: `WFShowResultAction` → `is.workflow.actions.showresult`

### Irregular Mappings

Some actions have non-standard mappings:

| Class Name | Identifier |
|------------|-----------|
| `WFRepeatAction` | `is.workflow.actions.repeat.count` |
| `WFForEachRepeatAction` | `is.workflow.actions.repeat.each` |
| `WFFiniteRepeatAction` | `is.workflow.actions.repeat.count` |
| `WFAskForInputAction` | `is.workflow.actions.ask` |
| `WFTextAction` | `is.workflow.actions.gettext` |
| `WFConditionalAction` | `is.workflow.actions.conditional` |
| `WFChooseFromMenuAction` | `is.workflow.actions.choosefrommenu` |
| `WFGetFileAction` | `is.workflow.actions.documentpicker.open` |
| `WFSelectFilesAction` | `is.workflow.actions.documentpicker.open` |
| `WFSaveFileAction` | `is.workflow.actions.documentpicker.save` |
| `WFGetCurrentWeatherConditionsAction` | `is.workflow.actions.weather.currentconditions` |
| `WFGetWeatherForecastAction` | `is.workflow.actions.weather.forecast` |
| `WFContentItemFilterAction` | `is.workflow.actions.filter.contentitems` |
| `WFGetUpcomingCalendarItemsAction` | `is.workflow.actions.getupcomingevents` |
| `WFAppendFileAction` | `is.workflow.actions.file.append` (was `appendfile` in older versions) |
| Modern file actions | `is.workflow.actions.file.createfolder`, `is.workflow.actions.file.delete`, `is.workflow.actions.file.getfoldercontents` |
| Modern text actions | `is.workflow.actions.text.combine`, `is.workflow.actions.text.match`, `is.workflow.actions.text.replace`, `is.workflow.actions.text.split`, `is.workflow.actions.text.trimwhitespace` |
| Modern dictionary actions | `is.workflow.actions.getvalueforkey`, `is.workflow.actions.setvalueforkey` |
| Modern property actions | `is.workflow.actions.properties.*`, `is.workflow.actions.setters.*` |

---

## Actions by Category

### Text & Input

| Identifier | Class | Description |
|------------|-------|-------------|
| `gettext` | WFTextAction | Create a text value |
| `ask` | WFAskForInputAction | Ask user for input |
| `askllm` | WFAskLLMAction | Use AI model (Apple Intelligence) |
| `comment` | WFCommentAction | Add a comment (no effect) |
| `dictatetext` | WFDictateTextAction | Dictate text |
| `showresult` | WFShowResultAction | Display result to user |
| `alert` | WFAlertAction | Show alert dialog |
| `notification` | WFNotificationAction | Send notification |
| `speaktext` | WFSpeakTextAction | Speak text aloud |
| `translatetext` | WFTranslateTextAction | Translate text |
| `detectlanguage` | WFDetectLanguageAction | Detect language |
| `base64encode` | WFBase64EncodeAction | Encode or decode Base64 |
| `detect.text` | WFDetectTextAction | Get text from input |
| `text.combine` | WFTextCombineAction | Combine text/list items |
| `text.match` | WFTextMatchAction | Match text with a pattern |
| `text.match.getgroup` | WFTextMatchGetGroupAction | Get a capture group from matches |
| `text.replace` | WFTextReplaceAction | Replace text |
| `text.split` | WFTextSplitAction | Split text |
| `text.trimwhitespace` | WFTrimWhitespaceAction | Trim whitespace |
| `gethtmlfromrichtext` | WFGetHTMLFromRichTextAction | Convert rich text to HTML |
| `getrichtextfromhtml` | WFGetRichTextFromHTMLAction | Convert HTML to rich text |
| `getrichtextfrommarkdown` | WFGetRichTextFromMarkdownAction | Convert Markdown to rich text |

### Variables

| Identifier | Class | Description |
|------------|-------|-------------|
| `setvariable` | WFSetVariableAction | Set a variable |
| `getvariable` | WFGetVariableAction | Get a variable |
| `appendvariable` | WFAppendVariableAction | Append to variable |
| `nothing` | WFNothingAction | Do nothing (pass-through) |

### Control Flow

| Identifier | Class | Description |
|------------|-------|-------------|
| `repeat.count` | WFRepeatAction | Repeat N times |
| `repeat.each` | WFForEachRepeatAction | Repeat for each item |
| `conditional` | WFConditionalAction | If/Otherwise |
| `choosefrommenu` | WFChooseFromMenuAction | Menu with cases |
| `choosefromlist` | WFChooseFromListAction | Choose from list |
| `exit` | WFExitAction | Exit shortcut |
| `output` | WFOutputAction | Set output |

### Files & Documents

| Identifier | Class | Description |
|------------|-------|-------------|
| `file` | WFFileAction | Create file reference |
| `documentpicker.open` | WFSelectFilesAction | Open file picker |
| `documentpicker.save` | WFSaveFileAction | Save file |
| `getfoldercontents` | WFGetFolderContentsAction | List folder contents |
| `createfolder` | WFCreateFolderAction | Create folder |
| `deletefile` | WFDeleteFileAction | Delete file |
| `movefile` | WFMoveFileAction | Move file |
| `renamefile` | WFRenameFileAction | Rename file |
| `file.append` | WFAppendFileAction | Append to text file (was `appendfile` in older versions) |
| `makearchive` | WFMakeArchiveAction | Create archive |
| `extractarchive` | WFExtractArchiveAction | Extract archive |

### Web & URLs

| Identifier | Class | Description |
|------------|-------|-------------|
| `url` | WFURLAction | Create URL |
| `downloadurl` | WFDownloadURLAction | Get contents of URL |
| `openurl` | WFOpenURLAction | Open URL |
| `expandurl` | WFExpandURLAction | Expand shortened URL |
| `geturlheaders` | WFGetURLHeadersAction | Get URL headers |
| `urlgetcomponent` | WFURLGetComponentAction | Get URL component |
| `urlencode` | WFURLEncodeAction | URL encode |
| `getwebpage` | WFGetWebPageAction | Get web page |
| `searchweb` | WFSearchWebAction | Search web |

### Apps & System

| Identifier | Class | Description |
|------------|-------|-------------|
| `openapp` | WFOpenAppAction | Open app |
| `quitapp` | WFQuitAppAction | Quit app |
| `hideapp` | WFHideAppAction | Hide app |
| `getcurrentapp` | WFGetCurrentAppAction | Get current app |
| `runworkflow` | WFRunWorkflowAction | Run another shortcut |
| `runshellscript` | WFRunShellScriptAction | Run shell script |
| `runosascript` | WFRunOSAScriptAction | Run AppleScript |
| `getdevicedetails` | WFGetDeviceDetailsAction | Get device info |
| `batterylevel` | WFBatteryLevelAction | Get battery level |
| `getclipboard` | WFGetClipboardAction | Get clipboard |
| `setclipboard` | WFSetClipboardAction | Set clipboard |

### Lists & Data

| Identifier | Class | Description |
|------------|-------|-------------|
| `list` | WFListAction | Create list |
| `dictionary` | WFDictionaryAction | Create dictionary |
| `getdictionaryvalue` | WFGetDictionaryValueAction | Get dictionary value |
| `setdictionaryvalue` | WFSetDictionaryValueAction | Set dictionary value |
| `getvalueforkey` | WFGetDictionaryValueAction | Sample-verified modern dictionary get |
| `setvalueforkey` | WFSetDictionaryValueAction | Sample-verified modern dictionary set |
| `detect.dictionary` | WFDetectDictionaryAction | Get dictionary from input |
| `getitemfromlist` | WFGetItemFromListAction | Get item from list |
| `count` | WFCountAction | Count items |
| `filter.contentitems` | WFContentItemFilterAction | Filter content |

### Numbers & Math

| Identifier | Class | Description |
|------------|-------|-------------|
| `number` | WFNumberAction | Create number |
| `calculate` | WFCalculateAction | Calculate |
| `calculatestatistics` | WFCalculateStatisticsAction | Statistics |
| `randomnumber` | WFRandomNumberAction | Random number |
| `roundnumber` | WFRoundNumberAction | Round number |
| `math` | WFMathAction | Perform one math operation |
| `measurementcreate` | WFMeasurementCreateAction | Create measurement |
| `measurementconvert` | WFMeasurementConvertAction | Convert measurement |

### Date & Time

| Identifier | Class | Description |
|------------|-------|-------------|
| `date` | WFDateAction | Create date |
| `formatdate` | WFFormatDateAction | Format date |
| `format.date` | WFFormatDateAction | Sample-verified modern format date identifier |
| `adjustdate` | WFAdjustDateAction | Adjust date |
| `converttimezone` | WFConvertTimeZoneAction | Convert timezone |
| `timeuntildate` | WFTimeUntilDateAction | Time between dates |
| `gettimebetweendates` | WFTimeUntilDateAction | Sample-verified time-between-dates identifier |
| `delay` | WFDelayAction | Wait |
| `waittoreturn` | WFWaitToReturnAction | Wait to return |

### Calendar & Reminders

| Identifier | Class | Description |
|------------|-------|-------------|
| `addnewevent` | WFAddNewEventAction | Create event |
| `getupcomingevents` | WFGetUpcomingCalendarItemsAction | Get upcoming events |
| `removecalendaritems` | WFRemoveCalendarItemsAction | Remove calendar items |
| `filter.calendarevents` | WFContentItemFilterAction | Find/filter calendar events |
| `properties.calendarevents` | WFContentItemPropertiesAction | Get calendar event property |
| `setters.calendarevents` | WFContentItemSetterAction | Set calendar event property |
| `addnewreminder` | WFAddNewReminderAction | Create reminder |
| `showreminderslist` | WFShowRemindersListAction | Show reminders |
| `reminders.showlist` | WFShowRemindersListAction | Sample-verified reminders list identifier |
| `filter.reminders` | WFContentItemFilterAction | Find/filter reminders |
| `properties.reminders` | WFContentItemPropertiesAction | Get reminder property |
| `setters.reminders` | WFContentItemSetterAction | Set reminder property |

### Weather & Location

| Identifier | Class | Description |
|------------|-------|-------------|
| `weather.currentconditions` | WFGetCurrentWeatherConditionsAction | Current weather |
| `weather.forecast` | WFGetWeatherForecastAction | Weather forecast |
| `getcurrentlocation` | WFGetCurrentLocationAction | Current location |
| `location` | WFLocationAction | Create location |
| `getdirections` | WFGetDirectionsAction | Get directions |
| `getdistance` | WFGetDistanceAction | Get distance |
| `searchmaps` | WFSearchMapsAction | Search maps |

### Media

| Identifier | Class | Description |
|------------|-------|-------------|
| `takephoto` | WFTakePhotoAction | Take photo |
| `takevideo` | WFTakeVideoAction | Take video |
| `selectphoto` | WFSelectPhotoAction | Select photos |
| `detect.images` | WFDetectImagesAction | Get images from input |
| `getlatestphotos` | WFGetLatestPhotosAction | Get latest photos |
| `filter.photos` | WFContentItemFilterAction | Find/filter photos (see [filters.md](filters.md)) |
| `savetocameraroll` | WFSaveToCameraRollAction | Save to camera roll |
| `deletephotos` | WFDeletePhotosAction | Delete photos (**uses `photos` param, not `WFInput`**) |
| `playmusic` | WFPlayMusicAction | Play music |
| `playpause` | WFPlayPauseAction | Play/Pause |
| `skipsong` | WFSkipSongAction | Skip song |
| `recordaudio` | WFRecordAudioAction | Record audio |
| `playsound` | WFPlaySoundAction | Play sound |

### Images

| Identifier | Class | Description |
|------------|-------|-------------|
| `imageresize` | WFImageResizeAction | Resize image |
| `image.resize` | WFImageResizeAction | Sample-verified modern resize identifier |
| `imagecrop` | WFImageCropAction | Crop image |
| `imagerotate` | WFImageRotateAction | Rotate image |
| `imageflip` | WFImageFlipAction | Flip image |
| `imageconvert` | WFImageConvertAction | Convert image |
| `image.convert` | WFImageConvertAction | Sample-verified modern convert identifier |
| `imagecombine` | WFImageCombineAction | Combine images |
| `overlayimage` | WFOverlayImageAction | Overlay image |
| `overlaytext` | WFOverlayTextAction | Overlay text |
| `imageremovebackground` | WFImageRemoveBackgroundAction | Remove background |
| `maskimage` | WFMaskImageAction | Mask image |
| `extracttextfromimage` | WFExtractTextFromImageAction | OCR |

### PDF

| Identifier | Class | Description |
|------------|-------|-------------|
| `makepdf` | WFMakePDFAction | Create PDF |
| `splitpdf` | WFSplitPDFAction | Split PDF |
| `compresspdf` | WFCompressPDFAction | Compress PDF |
| `gettextfrompdf` | WFGetTextFromPDFAction | Extract text from PDF |
| `makeimagefrompdfpage` | WFMakeImageFromPDFPageAction | PDF page to image |

### Sharing & Communication

| Identifier | Class | Description |
|------------|-------|-------------|
| `share` | WFShareAction | Share |
| `airdrop` | WFAirDropAction | AirDrop |
| `sendmessage` | WFSendMessageAction | Send message |
| `sendemail` | WFSendEmailAction | Send email |
| `startcall` | WFStartCallAction | Start call |
| `contacts` | WFContactsAction | Get contacts |
| `selectcontacts` | WFSelectContactsAction | Select contacts |
| `detect.contacts` | WFDetectContactsAction | Get contacts from input |
| `detect.phonenumber` | WFDetectPhoneNumberAction | Get phone numbers from input |
| `filter.contacts` | WFContentItemFilterAction | Find/filter contacts |
| `properties.contacts` | WFContentItemPropertiesAction | Get contact property |

### Settings

| Identifier | Class | Description |
|------------|-------|-------------|
| `setappearance` | WFSetAppearanceAction | Set light/dark mode |
| `setwifi` | WFSetWiFiAction | Set WiFi |
| `setcellulardata` | WFSetCellularDataAction | Set cellular data |
| `setlowpowermode` | WFSetLowPowerModeAction | Set low power mode |
| `setvolume` | WFSetVolumeAction | Set volume |
| `toggledonotdisturb` | WFToggleDoNotDisturbAction | Toggle Do Not Disturb |
| `setorientationlock` | WFSetOrientationLockAction | Set orientation lock |
| `setwallpaper` | WFSetWallpaperAction | Set wallpaper |
| `getwifi` | WFGetNetworkDetailsAction | Get Wi-Fi or cellular network details |
| `timer.start` | WFStartTimerAction | Start timer |

### Sample-Verified File and Document Variants

These variants were observed in current exported shortcuts and should be preferred over older inferred names when matching the same UI action.

| Identifier | Class / Family | Description |
|------------|----------------|-------------|
| `file.createfolder` | WFCreateFolderAction | Create folder |
| `file.delete` | WFDeleteFileAction | Delete file |
| `file.getfoldercontents` | WFGetFolderContentsAction | Get folder contents |
| `filter.files` | WFContentItemFilterAction | Find/filter files |
| `properties.files` | WFContentItemPropertiesAction | Get file property |
| `makezip` | WFMakeArchiveAction | Make ZIP archive |
| `previewdocument` | WFQuickLookAction | Preview document |
| `appendnote` | WFAppendNoteAction | Append input to a note |

---

## Production Sample Verified Identifiers

The following identifiers were present in the Momo, Vector Config, or Vector exported shortcuts and were missing from the earlier seed table. Parameter keys are shown from the sample plists only; do not treat them as a complete schema.

| Identifier | Count | Samples | Observed parameter keys |
|------------|------:|---------|-------------------------|
| `appendnote` | 5 | Momo | `AppIntentDescriptor, UUID, WFInput, WFNote` |
| `base64encode` | 6 | Momo, Vector | `UUID, WFBase64LineBreakMode, WFEncodeMode, WFInput` |
| `detect.contacts` | 1 | Momo | `UUID, WFInput` |
| `detect.dictionary` | 13 | Momo, Vector | `CustomOutputName, UUID, WFInput` |
| `detect.images` | 2 | Momo | `UUID, WFInput` |
| `detect.number` | 1 | Momo | `UUID, WFInput` |
| `detect.phonenumber` | 2 | Vector | `UUID, WFInput` |
| `detect.text` | 13 | Momo, Vector | `UUID, WFInput` |
| `file.createfolder` | 1 | Vector | `UUID, WFFilePath` |
| `file.delete` | 6 | Momo, Vector, Vector Config | `UUID, WFDeleteImmediatelyDelete, WFInput` |
| `file.getfoldercontents` | 2 | Vector, Vector Config | `UUID, WFFolder` |
| `filter.calendarevents` | 2 | Momo | `UUID, WFContentItemFilter, WFContentItemLimitEnabled, WFContentItemLimitNumber, WFContentItemSortOrder, WFContentItemSortProperty` |
| `filter.contacts` | 2 | Vector | `UUID, WFContentItemFilter, WFContentItemLimitEnabled, WFContentItemLimitNumber, WFContentItemSortOrder, WFContentItemSortProperty` |
| `filter.files` | 1 | Vector | `UUID, WFContentItemInputParameter, WFContentItemLimitEnabled, WFContentItemSortOrder, WFContentItemSortProperty` |
| `filter.notes` | 2 | Momo | `AppIntentDescriptor, UUID, WFContentItemFilter, WFContentItemInputParameter, WFContentItemLimitEnabled, WFContentItemLimitNumber, WFContentItemSortOrder, WFContentItemSortProperty` |
| `filter.reminders` | 10 | Momo | `CustomOutputName, UUID, WFContentItemFilter, WFContentItemInputParameter, WFContentItemLimitEnabled, WFContentItemLimitNumber, WFContentItemSortOrder, WFContentItemSortProperty` |
| `format.date` | 4 | Momo | `UUID, WFDate, WFDateFormat, WFDateFormatStyle, WFLocale, WFTimeFormatStyle` |
| `gethtmlfromrichtext` | 3 | Vector, Vector Config | `UUID, WFInput, WFMakeFullDocument` |
| `getrichtextfromhtml` | 1 | Momo | `UUID, WFHTML` |
| `getrichtextfrommarkdown` | 5 | Momo, Vector | `UUID, WFInput` |
| `gettimebetweendates` | 5 | Momo | `UUID, WFInput, WFTimeUntilFromDate, WFTimeUntilUnit` |
| `getvalueforkey` | 138 | Momo, Vector | `CustomOutputName, UUID, WFDictionaryKey, WFGetDictionaryValueType, WFInput` |
| `getwifi` | 2 | Vector | `CustomOutputName, UUID, WFCellularDetail, WFNetworkDetailsNetwork, WFWiFiDetail` |
| `image.convert` | 7 | Momo, Vector | `UUID, WFImageCompressionQuality, WFImageFormat, WFImagePreserveMetadata, WFInput` |
| `image.resize` | 3 | Momo | `UUID, WFImage, WFImageResizeKey, WFImageResizePercentage` |
| `makezip` | 1 | Vector Config | `UUID, WFArchiveFormat, WFInput, WFZIPName` |
| `math` | 1 | Vector | `UUID, WFInput, WFMathOperand, WFMathOperation` |
| `previewdocument` | 8 | Vector, Vector Config | `WFInput` |
| `properties.calendarevents` | 1 | Momo | `UUID, WFContentItemPropertyName, WFInput` |
| `properties.contacts` | 9 | Vector | `UUID, WFContentItemPropertyName, WFInput` |
| `properties.files` | 9 | Vector, Vector Config | `UUID, WFContentItemPropertyName, WFInput` |
| `properties.reminders` | 1 | Momo | `UUID, WFContentItemPropertyName, WFInput` |
| `reminders.showlist` | 1 | Momo | `WFList` |
| `setters.calendarevents` | 8 | Momo | `Mode, UUID, WFCalendarEventContentItemDuration, WFCalendarEventContentItemEndDate, WFCalendarEventContentItemNotes, WFCalendarEventContentItemTitle, WFContentItemPropertyName, WFInput` |
| `setters.reminders` | 8 | Momo | `Mode, UUID, WFContentItemPropertyName, WFInput, WFReminderContentItemDueDate, WFReminderContentItemIsCompleted, WFReminderContentItemTitle` |
| `setvalueforkey` | 14 | Momo, Vector | `UUID, WFDictionary, WFDictionaryKey, WFDictionaryValue` |
| `text.combine` | 13 | Momo, Vector | `Show-text, UUID, WFTextCustomSeparator, WFTextSeparator, text` |
| `text.match` | 7 | Momo | `UUID, WFMatchTextCaseSensitive, WFMatchTextPattern, text` |
| `text.match.getgroup` | 1 | Momo | `CustomOutputName, UUID, matches` |
| `text.replace` | 15 | Momo | `UUID, WFInput, WFReplaceTextCaseSensitive, WFReplaceTextFind, WFReplaceTextRegularExpression, WFReplaceTextReplace` |
| `text.split` | 8 | Momo, Vector | `Show-text, UUID, WFTextCustomSeparator, WFTextSeparator, text` |
| `text.trimwhitespace` | 2 | Vector | `UUID, WFInput` |
| `timer.start` | 2 | Momo, Vector | `AppIntentDescriptor, IntentAppDefinition, UUID, WFDuration` |

## All WF Identifiers Seen in the Three Production Samples

This table is intentionally redundant with the category tables. It makes the sample coverage easy to search and gives a quick signal for how common each identifier is in the reference shortcuts.

| Identifier | Count | Samples |
|------------|------:|---------|
| `addnewevent` | 5 | Momo, Vector |
| `addnewreminder` | 14 | Momo, Vector |
| `adjustdate` | 1 | Momo |
| `alert` | 90 | Momo, Vector, Vector Config |
| `appendnote` | 5 | Momo |
| `appendvariable` | 30 | Momo, Vector |
| `ask` | 25 | Momo, Vector, Vector Config |
| `base64encode` | 6 | Momo, Vector |
| `calculateexpression` | 4 | Momo, Vector |
| `choosefromlist` | 8 | Momo, Vector Config |
| `choosefrommenu` | 174 | Momo, Vector, Vector Config |
| `comment` | 15 | Momo |
| `conditional` | 636 | Momo, Vector, Vector Config |
| `count` | 17 | Momo, Vector |
| `date` | 1 | Momo |
| `delay` | 3 | Momo, Vector |
| `detect.contacts` | 1 | Momo |
| `detect.dictionary` | 13 | Momo, Vector |
| `detect.images` | 2 | Momo |
| `detect.number` | 1 | Momo |
| `detect.phonenumber` | 2 | Vector |
| `detect.text` | 13 | Momo, Vector |
| `dictatetext` | 6 | Momo, Vector |
| `dictionary` | 22 | Momo, Vector |
| `documentpicker.open` | 29 | Momo, Vector, Vector Config |
| `documentpicker.save` | 25 | Momo, Vector, Vector Config |
| `downloadurl` | 25 | Momo, Vector |
| `exit` | 68 | Momo, Vector, Vector Config |
| `extracttextfromimage` | 1 | Vector |
| `file` | 1 | Momo |
| `file.createfolder` | 1 | Vector |
| `file.delete` | 6 | Momo, Vector, Vector Config |
| `file.getfoldercontents` | 2 | Vector, Vector Config |
| `filter.calendarevents` | 2 | Momo |
| `filter.contacts` | 2 | Vector |
| `filter.files` | 1 | Vector |
| `filter.notes` | 2 | Momo |
| `filter.reminders` | 10 | Momo |
| `format.date` | 4 | Momo |
| `getcurrentapp` | 2 | Momo |
| `getdevicedetails` | 4 | Momo |
| `gethtmlfromrichtext` | 3 | Vector, Vector Config |
| `getitemfromlist` | 12 | Momo, Vector |
| `getitemtype` | 5 | Momo, Vector |
| `getrichtextfromhtml` | 1 | Momo |
| `getrichtextfrommarkdown` | 5 | Momo, Vector |
| `gettext` | 212 | Momo, Vector, Vector Config |
| `gettextfrompdf` | 1 | Vector |
| `gettimebetweendates` | 5 | Momo |
| `getvalueforkey` | 138 | Momo, Vector |
| `getvariable` | 4 | Vector |
| `getwifi` | 2 | Vector |
| `hash` | 1 | Momo |
| `image.convert` | 7 | Momo, Vector |
| `image.resize` | 3 | Momo |
| `list` | 5 | Momo, Vector |
| `makeimagefromrichtext` | 1 | Momo |
| `makespokenaudiofromtext` | 1 | Vector |
| `makezip` | 1 | Vector Config |
| `math` | 1 | Vector |
| `nothing` | 3 | Vector |
| `notification` | 12 | Momo, Vector |
| `number` | 14 | Momo, Vector |
| `openapp` | 2 | Momo |
| `openurl` | 13 | Momo, Vector, Vector Config |
| `output` | 1 | Vector Config |
| `previewdocument` | 8 | Vector, Vector Config |
| `properties.calendarevents` | 1 | Momo |
| `properties.contacts` | 9 | Vector |
| `properties.files` | 9 | Vector, Vector Config |
| `properties.reminders` | 1 | Momo |
| `recordaudio` | 1 | Momo |
| `reminders.showlist` | 1 | Momo |
| `repeat.count` | 10 | Momo, Vector |
| `repeat.each` | 54 | Momo, Vector, Vector Config |
| `runworkflow` | 10 | Momo, Vector, Vector Config |
| `savetocameraroll` | 1 | Vector |
| `selectphoto` | 2 | Momo, Vector |
| `sendemail` | 2 | Vector, Vector Config |
| `sendmessage` | 1 | Vector |
| `setclipboard` | 11 | Momo, Vector, Vector Config |
| `setitemname` | 11 | Momo, Vector, Vector Config |
| `setters.calendarevents` | 8 | Momo |
| `setters.reminders` | 8 | Momo |
| `setvalueforkey` | 14 | Momo, Vector |
| `setvariable` | 333 | Momo, Vector, Vector Config |
| `shownote` | 1 | Momo |
| `showresult` | 11 | Momo, Vector |
| `showwebpage` | 8 | Momo, Vector, Vector Config |
| `speaktext` | 2 | Vector |
| `statistics` | 1 | Vector |
| `takephoto` | 1 | Vector |
| `takescreenshot` | 5 | Momo, Vector |
| `text.combine` | 13 | Momo, Vector |
| `text.match` | 7 | Momo |
| `text.match.getgroup` | 1 | Momo |
| `text.replace` | 15 | Momo |
| `text.split` | 8 | Momo, Vector |
| `text.trimwhitespace` | 2 | Vector |
| `timer.start` | 2 | Momo, Vector |
| `url` | 6 | Momo, Vector, Vector Config |
| `urlencode` | 3 | Momo, Vector |
| `vibrate` | 12 | Momo |
| `weather.currentconditions` | 1 | Vector |

---

## Complete Identifier List

Seed action identifiers plus sample-verified additions (prefix `is.workflow.actions.` omitted). For newly discovered modern variants, prefer the exact identifier shown in "Production Sample Verified Identifiers".

```
addframetogif, addmusictoupnext, addnewcalendar, addnewcontact, addnewevent,
addnewreminder, addquickreminder, address, addtoplaylist, addtoreadinglist,
adjustdate, airdrop, alert, appattributed, appenddropboxfile, file.append,
appendtonote, appendvariable, appintentexecution, ask, askllm, batterylevel,
calculate, calculateexpression, calculatestatistics, changeplaybackdestination,
choosefromlist, choosefrommenu, clearupnext, coercion, comment, compactdialog,
compresspdf, conditional, configuredactionbuttonintent, configuredactionbuttonnothing,
configuredactionbuttonworkflow, configuredstaccato, configuredstaccatointent,
configuredstaccatonothing, configuredstaccatotophit, configuredstaccatoworkflow,
configuredsystem, configuredsystemcontrol, configuredsystemintent,
configuredsystemnothing, configuredsystemworkflow, connecttoservers, contacts,
contentattributionsetdebugger, contentitem, contentitemproperties, contentitemsetter,
controlflow, converttimezone, count, createfolder, createnote, createphotoalbum,
createplaylist, date, delay, deletefile, deletephotos, detectlanguage, dictatetext,
dictionary, displaysleep, documentpicker.open, documentpicker.save, downloadurl,
ejectdisk, emailaddress, encodemedia, evernoteappend, evernotecreate, evernotedelete,
evernotegetlink, evernotegetnotes, exit, expandurl, extractarchive,
extracttextfromimage, file, filter.contentitems, finderimageconvert,
findhealthsamples, focusconfigurationlink, folder, formatdate, formatfilesize,
formatnumber, generatehash, generatemachinereadablecode, getclass, getclipboard,
getcurrentapp, getcurrentlocation, getcurrentsafariwebpage, getcurrentsong,
getdevicedetails, getdictionaryvalue, getdirections, getdistance, getdropboxfile,
getemojiname, getepisodesforpodcast, getfilelink, getfocus, getfoldercontents,
getframesfromimage, gethalfwaypoint, gethomeaccessorystate, gethotspotpassword,
getipaddress, getitemfromlist, getitemname, getitemtype, getlatestphotoimport,
getlatestphotos, getmapslink, getmyworkflows, getnetworkdetails, getonscreencontent,
getparentdirectory, getparkedcarlocation, getplaylist, getpodcastsfromlibrary,
getposters, getselectedfinderfiles, gettext, gettextfrompdf, gettraveltime,
gettype, getupcomingevents, geturlheaders, getvariable, getwebpage, giphy,
handlecustomintent, handledonatedintent, handleintent, handlepaymentintent,
handlesystemintent, handoff, handoffplayback, hideapp, homeaccessory,
htmlfromrichtext, imagecombine, imageconvert, imagecrop, imageflip,
imageremovebackground, imageresize, imagerotate, imgurupload, importaudiofiles,
importtolightroom, input, instapaper, instapaperadd, instapaperget, interchange,
interchangescheme, intercom, labelfiles, link, linkactionserializedparametersforln,
linkbookschangepagenavigation, linkbookschangetheme, linkbooksfind,
linkbooksnavigatepages, linkcalculateappusageintent, linkcalendarclosescreen,
linkcalendarcreatecalendar, linkcalendardeletecalendar, linkcalendaropenscreen,
linkchangebinarysetting, linkclockcreatealarm, linkclockdeletealarm,
linkclocktogglealarm, linkcloseentity, linkcontentitemfilter, linkcopyentity,
linkcreateentity, linkdeleteentity, linkentity, linkfavoriteentity, linkfindhome,
linkfindhomecameraclip, linkfindhomedevice, linkfindhomeroom, linkfindhomescene,
linkfindhomezone, linkfindselectedhome, linkimageplaygroundgenerateimage,
linkinsertintelligencetext, linkipdatafindsportsevents,
linkmusicrecognitionrecognizemusic, linknavigatesequentially,
linknotesaddtagstonotes, linknoteschangesetting, linknotescreatefolder,
linknotescreatetag, linknotesdeletefolders, linknotesdeletetags, linknotesfind,
linknotesmovenotestofolder, linknotesopenaccount, linknotesopenapplocation,
linknotesopenfolder, linknotesopentag, linknotespinnotes,
linknotesremovetagsfromnotes, linkopencamera, linkopenentity,
linkphotoscreatememory, linkreminderscreatelist, linkremindersopensmartlist,
linkrunintelligencecommand, linksafarichangereadermodestate, linksafariclosetab,
linksafaricreateprivatetab, linksafaricreatetab, linksafaricreatetabgroup,
linksafarifindbookmarks, linksafarifindreadinglistitems, linksafarifindtabgroups,
linksafarifindtabs, linksafariopenbookmark, linksafariopenreadinglistitem,
linksafariopentab, linksafariopentabgroup, linksafariopenview, linksearch,
linkshortcutscreateicloudlink, linkshortcutscreateworkflow,
linkshortcutsdeleteworkflow, linkshortcutsresetcellulardatastatistics,
linkshortcutssearchshortcuts, linkshortcutssetdataroaming, linkshortcutssetdefaultline,
linkshortcutstogglecellularplan, linkstartstopwatch, linkstartworkout,
linktogglehomeaccessory, linkvisualintelligencecamera,
linkvoicememoschangerecordingplaybacksetting, linkvoicememoscreatefolder,
linkvoicememosdeletefolders, linkvoicememosdeleterecordings, linkvoicememosopenfolder,
linkvoicememosopenrecording, linkvoicememosplayrecording, linkvoicememosrecordingfind,
linkvoicememossearchrecordings, linkwritingtools, linkwritingtoolsadjusttone,
linkwritingtoolsformatlist, linkwritingtoolsformattable, linkwritingtoolsproofread,
linkwritingtoolsrewrite, linkwritingtoolssummarize, list, location, lockapp,
lockscreen, loghealthsample, logoutuser, logworkout, makearchive, makediskimage,
makegif, makeimagefrompdfpage, makeimagefromrichtext, makepdf,
makespokenaudiofromtext, makevideofromgif, markdownfromrichtext, markup, maskimage,
measurementconvert, measurementcreate, missing, mountdiskimage, movefile, movewindow,
nothing, notification, number, openapp, openin, openincalendar, openurl,
openuseractivity, openxcallbackurl, output, overlayimage, overlaytext,
overridablelink, phonenumber, pinboardadd, pinboardget, playmusic, playpause,
playpodcast, playsound, pocketadd, pocketget, print, quicklook, quitapp,
randomnumber, recognizemusic, recordaudio, remoteappintentexecution, remotelink,
removecalendaritems, removephotofromalbum, renamefile, repeat.count, repeat.each,
replacetext, requestrideintent, requestuber, resizewindow, returntohomescreen,
revealfiles, reversiblelink, richtextfromhtml, richtextfrommarkdown, roundnumber,
rssfeed, rssfeedextract, runjavascriptonwebpage, runosascript, runshellscript,
runshortcutconfigurationintent, runshortcutintent, runsshscript, runworkflow,
savedropboxfile, savetocameraroll, scanmachinereadablecode, searchitunes,
searchlocalbusinesses, searchmaps, searchweb, seek, selectcontacts, selectmusic,
selectphoto, sendemail, sendmessage, sendtogoodreader, setairdropreceiving,
setalwaysondisplay, setappearance, setcellulardata, setclipboard, setdictionaryvalue,
sethotspotpassword, setitemname, setlisteningmode, setlowpowermode, setorientationlock,
setparkedcar, setvariable, setvolume, setvpn, setwallpaper, setwifi, share,
shareextension, shazammedia, showdefinition, showinblindsquare, showinstore, shownote,
showpasswords, showreminderslist, showresult, showwebpage, shutdowndevice, skipsong,
sleepdevice, social, speaktext, splitpdf, splitscreenapp, spotlightsearch,
staccatolink, standaloneshortcut, startcall, startscreensaver, starttimer,
storageservice, storageserviceinput, subscribetopodcast, switchposter, takephoto,
takescreenshot, takevideo, textcomponents, timeuntildate, todoistadd,
toggledonotdisturb, translatetext, trelloaddcard, trellocreateboard, trellocreatelist,
trellogetitems, trimvideo, trimwhitespace, tumblrpost, ulyssesattach, url, urlencode,
urlgetcomponent, vibrate, viewcontentgraph, waittoreturn, watchmedo,
weather.currentconditions, weather.forecast, wordpresspost
```

---

## Common Parameter Patterns

### Text Parameters
```xml
<key>WFTextActionText</key>
<string>Your text here</string>
```

### Variable Reference Parameters
```xml
<key>Text</key>
<dict>
    <key>Value</key>
    <dict>
        <key>attachmentsByRange</key>
        <dict>
            <key>{0, 1}</key>
            <dict>
                <key>OutputUUID</key>
                <string>SOURCE-UUID</string>
                <key>OutputName</key>
                <string>Text</string>
                <key>Type</key>
                <string>ActionOutput</string>
            </dict>
        </dict>
        <key>string</key>
        <string>￼</string>
    </dict>
    <key>WFSerializationType</key>
    <string>WFTextTokenString</string>
</dict>
```

### Boolean Parameters
```xml
<key>WFSomeOption</key>
<true/>
```

### Number Parameters
```xml
<key>WFRepeatCount</key>
<integer>5</integer>
```

### Enum Parameters
```xml
<key>WFHTTPMethod</key>
<string>GET</string>
```

---

## Action-Specific Parameters

### Get Contents of URL (`is.workflow.actions.downloadurl`)

The `downloadurl` action (WFDownloadURLAction) makes HTTP requests. It supports various methods, headers, and body types.

#### Basic Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `UUID` | String | Unique identifier for variable references |
| `WFURL` | Variable ref or string | The URL to request |
| `WFHTTPMethod` | String | HTTP method: `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| `WFHTTPBodyType` | String | Body type: `JSON`, `Form`, `File` |

#### Headers (`WFHTTPHeaders`)

Headers use `WFDictionaryFieldValue` serialization with key-value items:

```xml
<key>WFHTTPHeaders</key>
<dict>
    <key>Value</key>
    <dict>
        <key>WFDictionaryFieldValueItems</key>
        <array>
            <dict>
                <key>WFItemType</key>
                <integer>0</integer>
                <key>WFKey</key>
                <dict>
                    <key>Value</key>
                    <dict>
                        <key>string</key>
                        <string>Content-Type</string>
                    </dict>
                    <key>WFSerializationType</key>
                    <string>WFTextTokenString</string>
                </dict>
                <key>WFValue</key>
                <dict>
                    <key>Value</key>
                    <dict>
                        <key>string</key>
                        <string>application/json</string>
                    </dict>
                    <key>WFSerializationType</key>
                    <string>WFTextTokenString</string>
                </dict>
            </dict>
        </array>
    </dict>
    <key>WFSerializationType</key>
    <string>WFDictionaryFieldValue</string>
</dict>
```

#### JSON Body (`WFJSONValues`)

When `WFHTTPBodyType` is `JSON`, use `WFJSONValues` for key-value pairs:

```xml
<key>WFJSONValues</key>
<dict>
    <key>Value</key>
    <dict>
        <key>WFDictionaryFieldValueItems</key>
        <array>
            <dict>
                <key>WFItemType</key>
                <integer>0</integer>
                <key>WFKey</key>
                <dict>
                    <key>Value</key>
                    <dict>
                        <key>string</key>
                        <string>prompt</string>
                    </dict>
                    <key>WFSerializationType</key>
                    <string>WFTextTokenString</string>
                </dict>
                <key>WFValue</key>
                <!-- Can be a static string or variable reference -->
                <dict>
                    <key>Value</key>
                    <dict>
                        <key>attachmentsByRange</key>
                        <dict>
                            <key>{0, 1}</key>
                            <dict>
                                <key>OutputUUID</key>
                                <string>ASK-ACTION-UUID</string>
                                <key>OutputName</key>
                                <string>Provided Input</string>
                                <key>Type</key>
                                <string>ActionOutput</string>
                            </dict>
                        </dict>
                        <key>string</key>
                        <string>￼</string>
                    </dict>
                    <key>WFSerializationType</key>
                    <string>WFTextTokenString</string>
                </dict>
            </dict>
        </array>
    </dict>
    <key>WFSerializationType</key>
    <string>WFDictionaryFieldValue</string>
</dict>
```

#### Form Body (`WFFormValues`)

When `WFHTTPBodyType` is `Form`, use `WFFormValues` (same structure as `WFJSONValues`).

#### File Body (`WFRequestVariable`)

When `WFHTTPBodyType` is `File`, use `WFRequestVariable` to reference file data:

```xml
<key>WFRequestVariable</key>
<dict>
    <key>Value</key>
    <dict>
        <key>attachmentsByRange</key>
        <dict>
            <key>{0, 1}</key>
            <dict>
                <key>OutputUUID</key>
                <string>FILE-SOURCE-UUID</string>
                <key>OutputName</key>
                <string>File</string>
                <key>Type</key>
                <string>ActionOutput</string>
            </dict>
        </dict>
        <key>string</key>
        <string>￼</string>
    </dict>
    <key>WFSerializationType</key>
    <string>WFTextTokenString</string>
</dict>
```

#### WFItemType Values

The `WFItemType` field in dictionary items indicates the value type:

| Value | Type |
|-------|------|
| 0 | Text/String |
| 1 | Number |
| 2 | Array |
| 3 | Dictionary |
| 4 | Boolean |

---

### Find Photos (`is.workflow.actions.filter.photos`)

Searches the photo library with filters. See [filters.md](filters.md) for complete filter documentation.

#### Key Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `UUID` | String | Action identifier for output reference |
| `WFContentItemFilter` | Dict | Filter conditions (see [filters.md](filters.md)) |
| `WFContentItemSortProperty` | String | Sort by: `Date Taken`, `Creation Date`, etc. |
| `WFContentItemSortOrder` | String | `Latest First` or `Oldest First` |
| `WFContentItemLimitEnabled` | Boolean | Enable result limit |
| `WFContentItemLimitNumber` | Integer | Max results to return |

#### Filter Properties for Photos

| Property | Type | Notes |
|----------|------|-------|
| `Is a Screenshot` | Boolean | Use this for screenshots, NOT media_type |
| `Media Type` | Enum | ONLY: `Image`, `Video`, `Live Photo` |
| `Date Taken` | Date | Use operators 1002 (is today), 1001 (is in the last) |
| `Album` | String | Album name |
| `Is Favorite` | Boolean | Favorited photos |
| `Is Hidden` | Boolean | Hidden photos |

#### Common Mistake: Screenshot Filtering

**WRONG:** Using `Media Type` = `Screenshot` - This value is invalid!

**CORRECT:** Use `Is a Screenshot` = `true` (boolean filter)

---

### Delete Photos (`is.workflow.actions.deletephotos`)

Deletes photos from the library.

#### Critical: Parameter Key

**The parameter key is `photos` (lowercase), NOT `WFInput`!**

This is an exception to the normal pattern where most actions use `WFInput`.

#### Correct Structure

```xml
<dict>
    <key>WFWorkflowActionIdentifier</key>
    <string>is.workflow.actions.deletephotos</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>UUID</key>
        <string>DELETE-UUID</string>
        <key>photos</key>  <!-- NOT WFInput! -->
        <dict>
            <key>Value</key>
            <dict>
                <key>OutputName</key>
                <string>Photos</string>
                <key>OutputUUID</key>
                <string>FIND-PHOTOS-UUID</string>
                <key>Type</key>
                <string>ActionOutput</string>
            </dict>
            <key>WFSerializationType</key>
            <string>WFTextTokenAttachment</string>
        </dict>
    </dict>
</dict>
```
