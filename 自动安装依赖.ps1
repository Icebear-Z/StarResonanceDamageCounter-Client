# Step 1: ����Ƿ�Ϊ����ԱȨ�ޣ�������ǣ�����������Ϊ����Ա
$IsAdmin = (New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $IsAdmin) {
    Write-Host "û�й���ԱȨ�ޣ������Թ���ԱȨ����������..."
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File $PSCommandPath" -Verb RunAs
    exit
}

# Step 2: ��ȡ��ǰ�ű����ڵ��ļ���·������ӵ���������
$scriptPath = $PSScriptRoot
$nodePath = "$scriptPath\nodejs\node-v22.18.0-win-x64"
$env:Path += ";$nodePath"
Write-Host "�ѽ� Node.js ·����ӵ�ϵͳ����������$nodePath"

# Step 3: ���� Corepack
Write-Host "���� Corepack..."
corepack enable

# Step 4: ����ִ�в���Ϊ RemoteSigned
Write-Host "����ִ�в���Ϊ RemoteSigned..."
try {
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Host "ִ�в����Ѹ���Ϊ RemoteSigned"
} catch {
    Write-Host "ִ�в�������ʧ�ܣ����ܱ��������Ը��ǡ�"
    Write-Host "��ǰִ�в��ԣ�"
    Get-ExecutionPolicy -List
}

# Step 5: ѯ���û�ȷ���Ƿ����
Write-Host "�ڴ˲����У������� a �����س�������..."
$input = Read-Host "������ a �����س���"
if ($input -ne "a") {
    Write-Host "������󣬽ű����˳�"
    exit
}

# Step 6: �л�����ǰ�ű����ڵ�Ŀ¼����װ pnpm
Write-Host "�л�����ǰ�ű����ڵ�Ŀ¼����װ pnpm..."
cd $scriptPath

# ȷ���л�����ȷĿ¼��ִ�а�װ
if (Test-Path "$scriptPath\package.json") {
    pnpm install
} else {
    Write-Host "δ�ҵ� package.json �ļ�����ȷ����ǰĿ¼����Ŀ�ĸ�Ŀ¼��"
    exit
}

# Step 7: �ȴ��û�ȷ�ϼ���
Write-Host "������ 'Do you want to continue?' ʱ������ y �����س�������..."

# Step 8: �ȴ���װ���
Write-Host "�ȴ� 5 �����Ա㰲װ���..."
Start-Sleep -Seconds 300

Write-Host "��װ��ɣ�"

# ���ִ��ڴ�
Read-Host -Prompt "�� Enter ���˳�"
