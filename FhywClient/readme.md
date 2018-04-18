
一：CMDB使用到linux命令
    1）查看平台
        uname
    2）查看系统版本
        cat /etc/redhat-release
    3）查看主机名
        hostname
    4）查看主板信息
        dmidecode -t system
    5）查看主板信息
        dmidecode -t system
    6）查看CPU信息
        cat /proc/cpuinfo
    7）查看MEN信息
        dmidecode -t  memory

    8）查看RAID信息
        查看是否有RAID
        情况1：检查有RAID
            lspci |grep RAID   #RAID卡型号LSI
            03:00.0 RAID bus controller: LSI Logic / Symbios Logic MegaRAID SAS 2208 [Thunderbolt] (rev 05)
        情况2：
            lspci |grep RAID为空

            cat /proc/scsi/scsi LSI Logical 说明有RAID
            －－－－－－－－－－－－－－－－－－
            Attached devices:
            Host: scsi0 Channel: 01 Id: 00 Lun: 00
              Vendor: LSI      Model: Logical Volume   Rev: 3000
              Type:   Direct-Access                    ANSI  SCSI revision: 06
            Host: scsi0 Channel: 00 Id: 00 Lun: 00
              Vendor: ATA      Model: INTEL SSDSC2BB24 Rev: 0370
              Type:   Direct-Access                    ANSI  SCSI revision: 06
            Host: scsi0 Channel: 00 Id: 01 Lun: 00
              Vendor: ATA      Model: INTEL SSDSC2BB24 Rev: 0370
              Type:   Direct-Access                    ANSI  SCSI revision: 06

         情况3：无RAID
            cat /proc/scsi/scsi
                Attached devices:
                Host: scsi1 Channel: 00 Id: 00 Lun: 00 硬盘
                  Vendor: ATA      Model: Samsung SSD 840  Rev: DXT0
                  Type:   Direct-Access                    ANSI  SCSI revision: 05
                Host: scsi7 Channel: 00 Id: 00 Lun: 00      #光驱
                  Vendor: AMI      Model: Virtual CDROM0   Rev: 1.00
                  Type:   CD-ROM                           ANSI  SCSI revision: 00
                Host: scsi9 Channel: 00 Id: 00 Lun: 00
                  Vendor: AMI      Model: Virtual HDISK0   Rev: 1.00
                  Type:   Direct-Access                    ANSI  SCSI revision: 00
                Host: scsi8 Channel: 00 Id: 00 Lun: 00
                  Vendor: AMI      Model: Virtual Floppy0  Rev: 1.00  软驱
                  Type:   Direct-Access                    ANSI  SCSI revision: 00



    9）查看硬盘信息
        MegaCli64  -PDList -aALL