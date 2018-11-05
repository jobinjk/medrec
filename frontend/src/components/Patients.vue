<template>
  <v-container fluid grid-list-lg>
    <!-- Headers -->
    <div>
      <v-layout row wrap>
        <v-flex xs12>
          <v-card tile flat>
            <v-card-text>
              <v-layout row wrap>
                <v-flex xs12>
                  <p class="headline">Patients</p>
                </v-flex>
                <v-flex xs12>
                  <v-layout>
                    <v-btn flat small color="primary" outline style="margin:0" @click.stop="addPatientView=true;error = {status:false,text:''};">New Patient</v-btn>
                  </v-layout>
                </v-flex>
              </v-layout>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </div>
    <!-- Content -->

    <!-- trials -->
    <v-layout row wrap>
      <v-flex xs4 v-for="item in patients.results" :key="item.id">
        <v-card color="grey lighten-4" class="elevation-7">
          <v-card-title class="headline blue-grey--text">
            {{item.name}}
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <span class="caption"><u>Patient ID:</u><br>
              <strong class="subheading blue-grey--text">{{item.id}}</strong>
            </span>
            <v-flex xs5>
                  <v-img
                    :src= 'origin+"/qr_images/patient_"+item.id+".png"'
                    height="125px"
                    contain
                  ></v-img>
            </v-flex>
            <br>
            <span class="caption">
              <label><u>Description</u></label><br>
              {{item.description}}
            </span>
            <br>
            <span class="caption">
              <label><u>Medication</u></label><br>
              <v-chip v-for="(med,index) in item.medication" :key="index" color="deep-purple darken-1" outline dark label>{{med}}</v-chip>
            </span>
            <br>
            <span class="caption">
              <label><u>Doctor's Name</u></label><br>
              {{item.added_by.username }}
            </span>
            <br>
            <v-tooltip top>
              <span slot="activator" class="grey--text">Created on:- {{  item.created_on | humanizeTime}}</span>
              <span> {{ item.created_on | calendarTime}} </span>
            </v-tooltip>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-btn icon @click.stop="editPatientView=true; editPatient=item;buildEditMedications(item); error = {status:false,text:''}">
              <v-icon color="amber darken-1">fa-edit</v-icon>
            </v-btn>
            <v-btn icon @click.native="deletePatient(item.id)">
              <v-icon color="error darken-1">fa-trash</v-icon>
            </v-btn> 
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout row wrap>
      <v-flex xs12 class="text-xs-center">
        <v-pagination color="deep-purple" circle v-model="patientPagination.page" :length="patients.pages" @input="fetchPatients"></v-pagination>
      </v-flex>
    </v-layout>

      <!-- Add new Patient form modal -->
      <v-layout row justify-center>
        <v-dialog v-model="addPatientView" persistent max-width="890" >
          <v-card>
            <v-card-title class="headline">Add Patient</v-card-title>
            <v-card-text>You can add a new Patient here. </v-card-text>
            <v-card-text>
              <v-form v-model="addPatientForm" ref="addPatientForm" @submit.prevent="addPatient" >
                <v-layout row wrap>
                  <v-flex xs12>

                    <v-text-field solo dark name="name" label="Name" placeholder="Enter Patients Name" id="name" v-model="newPatient.name" required></v-text-field>

                  </v-flex>
                  <v-flex xs12>
                    <v-text-field solo dark name="description" label="Description" placeholder="Enter Patients Description" id="description" v-model="newPatient.description" required></v-text-field>

                  </v-flex>
                  <v-flex xs12 v-for="(med,index) in newPatientMedication" :key="index">
                    <v-layout row wrap>
                      <v-flex xs11>
                        <v-text-field dark name="medication" solo label="Medication" placeholder="Enter Patients Medication" id="medication" v-model="med.item" required></v-text-field>
                      </v-flex>
                      <v-flex xs1>

                        <v-btn color="error" dark icon small @click.native="newPatientMedication.splice(index,1)"><v-icon small>delete</v-icon></v-btn>

                      </v-flex>
                    </v-layout>
                  </v-flex>
                  <v-btn color="teal" dark small @click.native="newPatientMedication.push({item:''})"><v-icon>add</v-icon>&nbsp; Add medication</v-btn>


                </v-layout>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="error darken-1" flat @click.native="newPatientMedication=[];addPatientView = false;">Cancel</v-btn>
                  <v-btn color="success darken-1" flat type="submit">Add</v-btn>
                </v-card-actions>
              </v-form>
            </v-card-text>
          </v-card>
        </v-dialog>
      </v-layout>

      <!-- Edit Patient form modal -->

      <v-layout row justify-center>
        <v-dialog v-model="editPatientView" persistent max-width="890" >
          <v-card>
            <v-card-title class="headline">Edit Patient</v-card-title>
            <v-card-text>You can edit a Patient here. </v-card-text>
            <v-card-text>
              <v-form v-model="editPatientForm" ref="editPatientForm" @submit.prevent="updatePatient" >
                <v-layout row wrap>
                  <v-flex xs12>
                    <v-text-field solo dark name="name" label="Name" placeholder="Enter Patients Name" id="name" v-model="editPatient.name" required></v-text-field>
                  </v-flex>
                  <v-flex xs12>
                    <v-text-field solo dark name="description" label="Description" placeholder="Enter Patients Description" id="description" v-model="editPatient.description" required></v-text-field>

                  </v-flex>
                  <v-flex xs12 v-for="(med,index) in editPatientMedication" :key="index">
                    <v-layout row wrap>
                      <v-flex xs11>
                        <v-text-field dark name="medication" solo label="Medication" placeholder="Enter Patients Medication" id="medication" v-model="med.item" required></v-text-field>
                      </v-flex>
                      <v-flex xs1>
                        <v-btn color="error" dark icon small @click.native="editPatientMedication.splice(index,1)">
                          <v-icon small>delete</v-icon>
                        </v-btn>
                      </v-flex>
                    </v-layout>
                  </v-flex>
                  <v-btn color="teal" dark small @click.native="editPatientMedication.push({item:''})">
                    <v-icon>add</v-icon>&nbsp; Add medication
                  </v-btn>
                </v-layout>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="error darken-1" flat @click.native="editPatient.meds=[];editPatientView = false;">Cancel</v-btn>
                  <v-btn color="success darken-1" flat type="submit">Save</v-btn>
                </v-card-actions>
              </v-form>
            </v-card-text>
          </v-card>
        </v-dialog>
      </v-layout>



    </v-container>


  </template>
  <script>
    export default {
      name: 'Patients',
      props: {
        wid: {
          type: String,
          default: null
        }
      },
      computed:{
        origin:function(){
          return process.env.BASE_ORIGIN
        }
      },
      data () {
        return {
          // image: require('http://0.0.0.0:8000/qr_images/patient_'+'{{item.id}}'+'.png'),
          addPatientView: false,
          editPatientView: false,
          addPatientForm: false,
          editPatientForm: false,
          patients: [],
          patientPagination:{page:1,rowsPerPage:10},
          newPatientMedication:[{item:''}],
          editPatientMedication: [],
          newPatient: {
            name: '',
            description: '',
            medication: [],
            patients:[]
          },
          editPatient: {
            name: '',
            description: '',
            medication: [],
            patients:[],
            meds:[{item:''}]
          },
          patientHeaders: [
          {
            text: 'Name',
            value: 'name',
            align: 'left',
            sortable: false
          },

          {
            text: 'Description',
            value: 'description',
            align: 'left',
            sortable: false

          },

          {
            text: 'Medication',
            value: 'medication',
            align: 'left',
            sortable: false

          },

          {
            text: 'Added_by',
            value: 'added_by',
            align: 'left',
            sortable: false
          },

          {
            text: 'Created_on',
            value: 'created_on',
            align: 'left',
            sortable: false
          },
          {
            text: 'Actions',
            value: 'actions',
            align: 'left',
            sortable: false
          }
          ],
          patients: []

        }
      },
      methods: {
        appendNewMed(){
          this.editPatient.meds.push({item:'new item'})
        // console.log(this.editPatient)
      },
      addPatient () {
        this.newPatient.medication = []
        for (var i = this.newPatientMedication.length - 1; i >= 0; i--) {
          this.newPatient.medication.push(this.newPatientMedication[i].item)          
        }
        var url = '/api/patients'
        this.$http.post(url, this.newPatient).then(
          (response) => {
            if (response.status === 200){
              this.addPatientView = false
              this.$refs.addPatientForm.reset()
              this.newPatientMedication = [{item:''}]
              this.fetchPatients(1)
              this.$notify({
                title: response.statusText,
                type: 'success',
                text: 'Hello, the Patient is added successfully!!!'
              })
            }
          },
          (err) => {
            this.$notify({
              title: err.response.statusText,
              type: 'error',
              text: 'Hello, the Patient adding failed!!!'

            })
          })
      },
      buildEditMedications(item){
        this.editPatientMedication = []
        for (var i = item.medication.length - 1; i >= 0; i--) {
          this.editPatientMedication.push({item:item.medication[i]})
        }
      },
      updatePatient () {
        this.editPatient.medication = []
        for (var i = this.editPatientMedication.length - 1; i >= 0; i--) {
          this.editPatient.medication.push(this.editPatientMedication[i].item)          
        }
        var url = '/api/patients/' + this.editPatient.id
        this.$http.put(url, this.editPatient).then(
          (response) => {
            if (response.status === 200){
              this.editPatientView = false
              this.$refs.editPatientForm.reset()
              this.editPatientMedication = [{item:''}]
              this.fetchPatients(1)
              this.$notify({
                title: response.statusText,
                type: 'success',
                text: 'Hello, the Patient is editted successfully!!!'
              })
            }
          },
          (err) => {
            this.$notify({
              title: err.response.statusText,
              type: 'error',
              text: 'Hello, the Patient editting failed!!!'
            })
          })
      },
      fetchPatients () {
        var url = ''
        var page = this.patientPagination.page
        var perPage = this.patientPagination.rowsPerPage
        var url = '/api/patients'
        url = url + '?page=' + page + '&perPage='+perPage
        this.$http.get(url).then(
          (response) => {
            this.patients.loading = false
            this.patients =response.data
          },
          (err) => {
            this.patients.loading = false
            this.$notify({
              title: err.response.statusText,
              type: 'error',
              text: 'Patient fetching failed!!!'
            })
          })
      },

      deletePatient (pid) {
        var url = '/api/patients/' + pid
        this.$http.delete(url).then(
          (response) => {
            if (response.status === 200) {
              this.fetchPatients()
              this.$notify({
                title: 'Patient Deleted',
                type: 'warn',
                text: 'Hello, the patient is deleted successfully!!!'
              })
            }
          },
          (err) => {
            this.$notify({
              title: err.response.statusText,
              type: 'error',
              text: 'Hello, the patient deleting failed!!!'
            }.bind(this))
          })
      }
    },
    created() {
      this.fetchPatients()
    }
  }

</script>