#!/bin/bash                                                               
                                                                          
# Check the credentials here first before running the script              
PROJECTDIR=$EDAKIA_PATH                                             
LOCALEXPORTDIR=$PROJECTDIR/files/send                              
OUTBOX=$LOCALEXPORTDIR/outbox                                             
INBOX=$LOCALEXPORTDIR/inbox                                               
LOGDIR=$LOCALEXPORTDIR/log                                                
PROCDIR=$LOCALEXPORTDIR/processing                                        
CONTROLDIR=$LOCALEXPORTDIR/control                                        
ERRORDIR=$LOCALEXPORTDIR/error                                            
ARCHIVEDIR=$LOCALEXPORTDIR/archive                                        
mkdir -p $INBOX $OUTBOX $LOGDIR $PROCDIR $CONTROLDIR $ERRORDIR $ARCHIVEDIR

TRANSACTIONURL=http://www.edakia.in/transactions.json
#TRANSACTIONURL=http://10.0.0.2:3000/transactions.json
                                                         
LOGFILE=`date '+%Y%m%d.log'`

# ========================================================
# DO NOT CHANGE anything below this line
# ========================================================

# ========================================================
# Helper functions for our scripts                 
# ========================================================
check_error() {
    if [ "$1" -ne "0" ]; then
        echo "Export $3:`date +\"%d-%m-%y:%T\"`: $2"
    return 1
    fi
  return 0
}
                                                                          
log_entry(){                                                              
  echo "Export $2:`date +"%d-%m-%y:%T"` :$1"                              
}                                                         
                                                          
file_exists(){                                            
  for file in $1/*.txt                                    
  do                                                     
    if [ -f "$file" ]; then                              
      return 0                                       
    fi                                               
    return 1                                         
  done                                      
} 

image_exists(){                                            
  for file in $1/*.jpg                                    
  do                                                     
    if [ -f "$file" ]; then                              
      return 0                                       
    fi                                               
    return 1                                         
  done                                      
} 

tiff_exists(){                                            
  for file in $1/*.tiff                                    
  do                                                     
    if [ -f "$file" ]; then                              
      return 0                                       
    fi                                               
    return 1                                         
  done                                      
}

export_tiff_to_jpg(){
	folder=`basename $1`
  convert -quality 60 $1/${folder}.tiff $1/${folder}.jpg
	rm $1/${folder}.tiff
}

rename_images(){
  i=0
  folder=`basename $1`
  for file in $1/*.JPG
  do                                                     
    if [ -f "$file" ]; then                              
      mv $file $1/${folder}_${i}.jpg                                
      i=`expr $i + 1`
    fi                                               
  done                                      
}

dir_exists(){                                             
  if [ "$(ls -A $1)" ]; then
    return 0
  else
    return 1
  fi
}

files_unrecognized(){
	echo "moving $1 to $CONTROLDIR/" 
	mv -f $1 $CONTROLDIR/
}

exec >> $LOGDIR/$LOGFILE 2>&1

# ========================================================
# PROGRAM start
# ========================================================

START=`date '+%d-%m-%Y %H:%M:%S'`
echo "===================================================="
echo "Starting script @ $START"
echo "Processing files in $OUTBOX"

# ========================================================                
# Check if internet is working                                         
# ========================================================                
sh ${PROJECTDIR}/scripts/internet.sh
if [ $? -eq 1 ]; then
  log_entry "No internet access" "ERROR"
  exit 0
fi 
# ========================================================                
# 1. moving outbox files to processing                                         
# ========================================================                
dir_exists $OUTBOX                                                         
check_error $? "Nothing to move to processing" "NOTICE"                 
ret_val=$?                                                
if [ "$ret_val" -ne "1" ]; then                           
  log_entry "moving files from outbox to processing" INFO  
  cp -r $OUTBOX/* $PROCDIR/                                 
  rm -r $OUTBOX/*                                          
fi  


# ========================================================                
# 2. Processing files to send to server                                         
# ========================================================                

script_ret_val=0

# Now process each file and ensure it was sent ok.
#for folder in `find $PROCDIR -type f -size +0`
for folder in `ls -A $PROCDIR`
do
  # ========================================================                
  # 2.a. Check if txt file exists or not                                         
  # ========================================================                

  file_exists $PROCDIR/$folder
  if [ "$?" -eq 1 ]; then
    log_entry "TXT file not exist in folder $PROCDIR/$folder" "ERROR" 
    files_unrecognized $PROCDIR/$folder
    continue 
  fi


  # ========================================================                
  # 2.b. Exporting image file from *.tiff to *.jpg                                         
  # ========================================================                
	tiff_exists $PROCDIR/$folder
  if [ "$?" -eq 0 ]; then
    log_entry "Exporting tiff to jpg $PROCDIR/$folder" "INFO"
    export_tiff_to_jpg $PROCDIR/$folder 
  fi
  

  # ========================================================                
  # 2.c. Check if image file exists or not                                         
  # ========================================================                

  image_exists $PROCDIR/$folder
  if [ "$?" -eq 1 ]; then
    log_entry "Scanned image file not exist in $PROCDIR/$folder" "ERROR"
    files_unrecognized $PROCDIR/$folder
    continue 
  fi

  # ========================================================                
  # 2.d. Read the corresponding transaction credentials                                         
  # ========================================================                
  file=$PROCDIR/$folder/$folder.txt
  image_file=`ls -tr $PROCDIR/$folder/*.jpg | tail -1`
  echo "File name: $file"
  echo "Image file: $image_file"

  lsof -w > /dev/null 2>&1 $file
  if [ "$?" -eq "0" ]; then
	# file is in use, so don't copy yet.
	echo "File $file is still in use, deferring the transfer for that file."
	continue
  fi
  
  lsof -w > /dev/null 2>&1 $image_file
  if [ "$?" -eq "0" ]; then
	# file is in use, so don't copy yet.
	echo "File $file is still in use, deferring the transfer for that file."
	continue
  fi

  sender=`sed -n 1p $file`
  password=`sed -n 2p $file`
  receiver=`sed -n 3p $file`

  # ========================================================                
  # 2.e. Curl to send the file with credentials                                         
  # ========================================================                
  response=$(curl --write-out %{http_code} --silent -u $sender:$password -F transaction[document_attributes][doc]=@$image_file -F transaction[receiver_mobile]=$receiver -F transaction[sender_mobile]=$sender $TRANSACTIONURL)
  echo $response
  if [ "$response" -ne "200" ]; then
	# Something went wrong with the CURL operation
	# Move processing file to error dir.
	echo "Error in transaction: moving $PROCDIR/$folder to $ERRORDIR/" 
	mv -f "$PROCDIR/$folder" "$ERRORDIR/"

	# Indicate there were errors
	script_ret_val=1
  else
	# File successfully transferred. Move file to archive dir
	echo "Successfully transfered: Archiving $PROCDIR/$folder"
	mv -f "$PROCDIR/$folder" "$ARCHIVEDIR/"
  fi
done

# ========================================================                
# 3. Remove old files
# ========================================================                

END=`date '+%d-%m-%Y %H:%M:%S'`
echo "Script exited @ $END with retval: ${script_ret_val}"

exit $script_ret_val
