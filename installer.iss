[Setup]
AppName=Nexus
AppVerName=Nexus
AppVersion=1.2
AppPublisher=Faraz Kayan Haque
DefaultDirName={autopf}\Nexus
DefaultGroupName=Nexus
OutputDir=installer_output
OutputBaseFilename=Nexus_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=nexus.ico
UninstallDisplayIcon={app}\Nexus.exe

[Files]
Source: "dist\Nexus.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Nexus"; Filename: "{app}\Nexus.exe"; IconFilename: "{app}\Nexus.exe"
Name: "{commondesktop}\Nexus"; Filename: "{app}\Nexus.exe"; IconFilename: "{app}\Nexus.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\Nexus.exe"; Description: "Launch Nexus"; Flags: nowait postinstall skipifsilent