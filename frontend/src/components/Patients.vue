<template>
  <v-container fluid grid-list-xs>
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
    <div>
      <v-layout row wrap>
        <v-flex xs12>
          <v-data-table :headers="patientHeaders" :items="patients.results" :loading="patients.loading" :total-items="patients.total" :pagination.sync="patientPagination">
            <template slot="items" slot-scope="props">
              <td>{{ props.item.name }}</td>
              <td>{{ props.item.description }}</td>
              <td>{{ props.item.medication }}</td>
              <td> <v-chip small label outline color="accent">{{ props.item.added_by.username }}</v-chip></td>
              <td>
                <v-tooltip top>
                  <span slot="activator" class="grey--text">{{  props.item.created_on | humanizeTime}}</span>
                  <span>{{ props.item.created_on | calendarTime}}</span>
                </v-tooltip>
              </td>
              <td>
                <v-btn icon small @click.stop="editPatientView=true; $refs.editPatientForm.reset(); editPatient=props.item;buildEditMedications(props.item); error = {status:false,text:''}">
                  <v-icon small color="amber darken-1">fa-edit</v-icon>
                </v-btn>
                <v-btn icon small @click.native="deletePatient(props.item.id)">
                  <v-icon small color="error darken-1">fa-trash</v-icon>
                </v-btn>                
              </td>
            </template>
          </v-data-table>
        </v-flex>
      </v-layout>
    </div>


    <!-- Add new Patient form modal -->
    <v-layout row justify-center>
      <v-dialog v-model="addPatientView" persistent max-width="890" >
        <v-card>
          <v-card-title class="headline">Add Patient</v-card-title>
          <v-card-text>You can add a new Patient here. </v-card-text>
          <v-card-text>
            <v-form v-model="addPatientForm" ref="addProjectForm" @submit.prevent="addPatient" >
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
                <v-btn color="error darken-1" flat @click.native="addPatientView = false;">Cancel</v-btn>
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
                    
                  <v-btn color="error" dark icon small @click.native="editPatientMedication.splice(index,1)"><v-icon small>delete</v-icon></v-btn>
                  
                  </v-flex>
                  </v-layout>
                </v-flex>
                    <v-btn color="teal" dark small @click.native="editPatientMedication.push({item:''})"><v-icon>add</v-icon>&nbsp; Add medication</v-btn>
                  

              </v-layout>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="error darken-1" flat @click.native="editPatientView = false;">Cancel</v-btn>
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
    data () {
      return {
        addPatientView: false,
        editPatientView: false,
        addPatientForm: false,
        editPatientForm: false,
        patients: [],
        patientPagination: {
          page:1,
          rowsPerPage: 5
        },
        newPatientMedication:[{item:''}],
        editPatientMedication: [],
        newPatient: {
          name: '',
          description: '',
          medication: '',
          patients:[]
        },
        editPatient: {
          name: '',
          description: '',
          medication: '',
          patients:[]
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
        }
        ],
        patients: []

      }
    },
    watch: {
      patientPagination: {
        handler () {
          this.fetchPatients()
        },
        deep: true
      }
    },

    methods: {
      addPatient () {
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
        for (var i = item.medication.length - 1; i >= 0; i--) {
          this.editPatientMedication.push({item:item.medication[i]})
        }
      },
      updatePatient () {
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
        url = url + '?page=' + page + '&perPage=' + perPage
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
              this.fetchPatients(1)
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
      },
      created () {

      },
      beforeMount () {
        this.fetchPatients()
      },
      mounted() {

      }
    }
  }

</script>