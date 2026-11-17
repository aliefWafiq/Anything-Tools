; Inno Setup Script
#define MyAppName "Anything"
#define MyAppVersion "1.0"
#define MyAppPublisher "MyOrg"
#define MyAppExeName "anything.exe"

[Setup]
AppId={{efd50612-dac2-4a58-9959-cdb894b5ce5f}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputBaseFilename=AnythingInstaller
Compression=lzma
SolidCompression=yes
; Add to PATH
ChangesEnvironment=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; Path assume built via PyInstaller in dist/
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
; Logic to append to PATH
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Check: NeedsAddPath

[Code]
const
  WM_SETTINGCHANGE = $001A;

function NeedsAddPath(): Boolean;
var
  Path: String;
begin
  RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', Path);
  Result := Pos(';' + ExpandConstant('{app}') + ';', ';' + Path + ';') = 0;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
    SendNotifyMessage(HWND_BROADCAST, WM_SETTINGCHANGE, 0, 0);
end;
